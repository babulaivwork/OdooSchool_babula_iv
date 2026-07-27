from lxml import etree
from markupsafe import Markup, escape

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.base.models.ir_qweb import QWebError


class QWebTutorialController(http.Controller):
    @http.route(
        '/qweb_tutorial/render',
        type='http',
        auth='public',
        methods=['POST'],
        website=True,
    )
    def render_qweb(self, **kw):
        model_name = kw.get('model_name', '')
        template_code = kw.get('template_code', '')
        rendered_html = Markup()

        if model_name and template_code:
            try:
                model = request.env[model_name]
                records = model.search([], limit=10)

                template_element = etree.fromstring(f"""
                <templates>
                    <t t-name="custom_template">{template_code}</t>
                </templates>
                """)

                rendered_html = request.env['ir.qweb']._render(
                    template_element,
                    {'docs': records},
                )
            except (KeyError, TypeError, ValueError, etree.XMLSyntaxError, QWebError, UserError) as error:
                rendered_html = Markup('<div class="alert alert-danger">Error: %s</div>') % escape(str(error))

        return request.make_response(rendered_html)

    @http.route(
        '/qweb_tutorial/render_new_window/<int:record_id>',
        type='http',
        auth='public',
        methods=['GET'],
        website=True,
    )
    def render_qweb_new_window(self, record_id, **kw):
        record = request.env['qweb.tutorial'].browse(record_id)
        if not record.exists():
            return request.not_found()

        qweb_template = """
        <t t-name="qweb_tutorial.render_template">
            <t t-call="web.frontend_layout">
                <div class="container py-4">
                    <t t-out="content"/>
                </div>
            </t>
        </t>
        """
        template_element = etree.fromstring(qweb_template)
        rendered_html = request.env['ir.qweb']._render(
            template_element,
            {'content': record.rendered_html or Markup()},
        )

        return request.make_response(rendered_html)
