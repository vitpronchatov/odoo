# -*- coding: utf-8 -*-

from openerp import fields, models


class ResPartnerKod(models.Model):
    _inherit = 'res.partner'

    kod_filii = fields.Char(string=u"Код філії", size=4)

#ResPartnerKod()
