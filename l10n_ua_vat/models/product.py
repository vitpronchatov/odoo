# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class ProductTemplUktZed(models.Model):
    _inherit = 'product.template'

    ukt_zed = fields.Char(related='product_variant_ids.ukt_zed',
                          string=u"Код УКТ ЗЕД",
                          help=u"Код згідно УКТ ЗЕД",
                          store=True)


class ProductUktZed(models.Model):
    _inherit = 'product.product'

    ukt_zed = fields.Char(string=u"Код УКТ ЗЕД",
                          help=u"Код згідно УКТ ЗЕД",
                          size=10)


class ProductUomCode(models.Model):

    uom_code = fields.Char(string=u"Код одиниць виміру",
                           help=u"Код згідно КСПОВО",
                           size=4)
