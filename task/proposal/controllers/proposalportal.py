from odoo import fields, http, _
from datetime import date
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.exceptions import AccessError, MissingError


class CustomerProposal(CustomerPortal):

    @http.route(['/my/proposal/<int:product>'], type='http', auth="public", website=True)
    def portal_order_page(self, product, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('proposal.order', product, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='sale.action_report_saleorder', download=download)

        if order_sudo:
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if isinstance(session_obj_date, date):
                session_obj_date = session_obj_date.isoformat()
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_quote_%s' % order_sudo.id] = now
                body = _('Proposal viewed by customer')
                _message_post_helper(res_model='proposal.order', res_id=order_sudo.id, message=body, token=order_sudo.access_token, message_type='notification', subtype="mail.mt_note", partner_ids=order_sudo.user_id.sudo().product.ids)

        values = {
                'proposal_order': order_sudo,
                'message': message,
                'token': access_token,
                'return_url': '/shop/payment/validate',
                'bootstrap_formatting': True,
                'partner_id': order_sudo.customer_name.id,
                'report_type': 'html',
            }
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id

        return request.render('proposal.porposal_portal_template', values)

    @http.route('/proposal/accepted/', type='json', auth='none')
    def proposal_order(self, data):
            for i in data:
                rec_id = int(i['rec_id'])
                stateobj = request.env['proposal.order'].sudo().search([('id', '=', rec_id)])
                line_id = int(i['line_id'])
                proposal_obj = request.env['proposal.orderline'].sudo().search([('id', '=', line_id)])
                stateobj.write({'state': i['state']})
                qty = float(i['accepted_quantity'])
                price = float(i['accepted_price'])
                proposal_obj.write({'accepted_quantity': qty, 'accepted_price': price})
            return True
