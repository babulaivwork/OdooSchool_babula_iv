from odoo import fields, models


class OSHrHospitalVisit(models.Model):
    _name = 'os.hr.hospital.visit'
    _description = 'Patient Visit'

    name = fields.Char(required=True, default='New Visit')
    active = fields.Boolean(default=True)
    result = fields.Text()
    description = fields.Text()
    patient_id = fields.Many2one(
        comodel_name='os.hr.hospital.patient',
        string='Patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='os.hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name='os.hr.hospital.disease',
        string='Disease',
    )
    visit_date = fields.Datetime(
        string='Visit Date',
        default=fields.Datetime.now,
        required=True,
    )
