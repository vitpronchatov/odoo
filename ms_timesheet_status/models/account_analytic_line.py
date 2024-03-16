# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    state = fields.Selection([
        ('open', 'Open'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
    ], string='State', default='open')

    def action_set_to_invoiced(self):
        self.write({'state': 'invoiced'})

    def action_set_to_paid(self):
        self.write({'state': 'paid'})

    def action_set_to_cancel(self):
        self.write({'state': 'cancel'})
