from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    price_unit = fields.Float(
        string='Price Unit per Hour',
        required=False)
