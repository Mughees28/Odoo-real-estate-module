from odoo import fields, models, api


class EstateProperties(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesman')
