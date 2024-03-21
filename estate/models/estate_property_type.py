from odoo import fields, models


class EstatePropertiesType(models.Model):
    _name = "estate.property.type"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)',
         'Property type name must be unique.')
    ]
