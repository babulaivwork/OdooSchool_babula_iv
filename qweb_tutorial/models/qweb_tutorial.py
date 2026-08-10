from ast import literal_eval

from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Domain

from odoo.addons.base.models.ir_qweb import QWebError


class QWebTutorial(models.Model):
    _name = 'qweb.tutorial'
    _description = 'QWeb Tutorial'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    model_id = fields.Many2one('ir.model', string='Model', ondelete='cascade')
    template_code = fields.Text(string='QWeb Template Code')
    domain = fields.Char(string='Domain', help='Domain for selecting records')
    rendered_html = fields.Html(string='Rendered HTML')
    pdf_attachment_id = fields.Binary(string='PDF Attachment')
    record_limit = fields.Integer(
        string='Record Limit',
        required=True,
        default=10,
    )

    @api.constrains('record_limit')
    def _check_record_limit(self):
        for record in self:
            if not 1 <= record.record_limit <= 100:
                raise ValidationError('The record limit must be between 1 and 100.')

    def _parse_domain(self):
        self.ensure_one()
        try:
            domain = literal_eval(self.domain or '[]')
        except (SyntaxError, ValueError) as error:
            raise UserError(f'Invalid domain: {error}') from error

        if not isinstance(domain, (list, tuple)):
            raise UserError('The domain must be a list or tuple.')
        return Domain(domain)

    def _render_template(self):
        self.ensure_one()
        model = self.env[self.model_id.model]
        example_records = model.search(
            self._parse_domain(),
            limit=self.record_limit,
        )
        values = {
            'docs': example_records,
            'model': model,
            'record': self,
        }
        template_code = f"<t t-name='custom_template'>{self.template_code}</t>"
        template_element = etree.fromstring(template_code)
        return self.env['ir.qweb']._render(template_element, values)

    def _compute_rendered_html(self):
        for record in self:
            if not record.template_code or not record.model_id:
                record.rendered_html = False
                continue

            try:
                record.rendered_html = record._render_template()
            except (KeyError, TypeError, ValueError, etree.XMLSyntaxError, QWebError, UserError) as error:
                raise UserError(f'Error rendering QWeb template: {error}') from error

    def action_render_qweb(self):
        self._compute_rendered_html()

    def action_render_qweb_new_window(self):
        self.ensure_one()
        self._compute_rendered_html()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/qweb_tutorial/render_new_window/{self.id}',
            'target': 'new',
        }
