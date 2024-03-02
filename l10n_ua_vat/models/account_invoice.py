# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class VatAccountInvoice(models.Model):

    def _get_taxinvoices_count(self):
        for invoice in self:
            if invoice.state not in ('open', 'paid'):
                invoice.tax_invoice_count = 0
            else:
                invoice.tax_invoice_count = len(invoice.tax_invoice_ids)
            return

    def _get_fully_tax_invoiced(self):
        for invoice in self:
            invoice._get_taxinvoices_count()
            if invoice.tax_invoice_count <= 0:
                invoice.fully_tax_invoiced = False
                return False
            inv_tax_amt = 0
            tax_inv_tax_amt = 0
            for tax in invoice.tax_line_ids:
                if tax.name.find(u"ПДВ") >= 0:
                    inv_tax_amt += tax.amount
            for tax_inv in invoice.tax_invoice_ids:
                tax_inv_tax_amt += tax_inv.amount_tax
            if inv_tax_amt <= tax_inv_tax_amt:
                invoice.fully_tax_invoiced = True
                return True
            else:
                invoice.fully_tax_invoiced = False
                return False

    tax_invoice_count = fields.Integer(
        string='# of Tax Invoices',
        compute='_get_taxinvoices_count',
        readonly=True)
    tax_invoice_ids = fields.One2many(
        'account.taxinvoice',
        'invoice_id',
        string='Tax Invoices',
        readonly=True,
        copy=False)
    fully_tax_invoiced = fields.Boolean(
        string='Fully Tax Invoiced',
        compute='_get_fully_tax_invoiced',
        readonly=True)

    def action_view_taxinvoices(self):
        self.ensure_one()
        tax_invoice_ids = self.mapped('tax_invoice_ids')
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object(
            'l10n_ua_vat.customer_tax_invoice_list_action')
        list_view_id = imd.xmlid_to_res_id(
            'l10n_ua_vat.tax_invoice_tree_view')
        form_view_id = imd.xmlid_to_res_id(
            'l10n_ua_vat.tax_invoice_form_view')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [
                         [list_view_id, 'tree'],
                         [form_view_id, 'form'],
                         [False, 'graph'],
                         [False, 'kanban'],
                         [False, 'calendar'],
                         [False, 'pivot']
                     ],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        if len(tax_invoice_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % tax_invoice_ids.ids
        elif len(tax_invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = tax_invoice_ids.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    def tax_invoice_create(self):
        for inv in self:
            ipn_partner = inv.partner_id.vat
            if ipn_partner:
                if ipn_partner == u"100000000000":
                    horig1 = True
                    htypr = '02'
                else:
                    horig1 = False
                    htypr = '00'
            else:
                raise UserError(_(u"Вкажіть ІПН у налаштуваннях контрагента."))
                return {}
            acc_ti = self.env['account.taxinvoice']
            ctx = dict(self._context)
            ctx['company_id'] = inv.company_id.id
            ctx['category'] = 'out_tax_invoice'
            ctx['state'] = 'draft'
            account = acc_ti.with_context(ctx)._default_account()
            tax_invoice = acc_ti.with_context(ctx).create({
                'state': 'draft',
                'h03': False,
                'horig1': horig1,
                'htypr': htypr,
                'date_vyp': inv.date,
                'number': None,
                'number1': None,
                'number2': inv.company_id.kod_filii or None,
                'kod_filii': inv.partner_id.kod_filii,
                'category': 'out_tax_invoice',
                'doc_type': 'pn',
                'partner_id': inv.partner_id.id,
                'ipn_partner': ipn_partner,
                'prych_zv': None,
                'signer_id': self.env.user.id,
                'currency_id': inv.currency_id.id,
                'journal_id': inv.journal_id.id,
                'company_id': inv.company_id.id,
                'account_id': account.id,
                'invoice_id': inv.id,
                'amount_tara': 0})

            # create tax invoice lines
            ti_line = self.env['account.taxinvoice.line']
            for line in inv.invoice_line_ids:
                for tax in line.invoice_line_tax_ids:
                    if line.quantity > 0 and tax.name.find(u"ПДВ") >= 0:
                        ti_l = ti_line.with_context(ctx).create({
                            'taxinvoice_id': tax_invoice.id,
                            'taxinvoice_line_tax_id': tax.id,
                            'account_id': tax.account_id.id or False,
                            'date_vynyk': inv.date,
                            'product_id': line.product_id.id,
                            'uom_id': line.uom_id.id,
                            'uom_code': line.uom_id.uom_code,
                            'price_unit': line.price_unit,
                            'discount': line.discount,
                            'quantity': line.quantity,
                            'ukt_zed': line.product_id.ukt_zed,
                            })
                        ti_l._compute_subtotal()
                    else:
                        continue
            tax_invoice._onchange_taxinvoice_line_ids()
            tax_invoice._compute_amount()
        return {}
