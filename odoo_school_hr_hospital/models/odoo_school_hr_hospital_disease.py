from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OSHrHospitalDisease(models.Model):
    _name = 'os.hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'
    _parent_store = True

    display_name = fields.Char(recursive=True)
    name = fields.Char()
    active = fields.Boolean(default=True)
    description = fields.Text()
    code = fields.Char()
    parent_id = fields.Many2one(
        comodel_name='os.hr.hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='set null',
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        comodel_name='os.hr.hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='disease_id',
        string='Visits',
    )

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        for disease in self:
            name_parts = [disease.parent_id.display_name, disease.name]
            disease.display_name = ' / '.join(name for name in name_parts if name)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if self._has_cycle():
            raise ValidationError('A disease hierarchy cannot contain cycles.')
