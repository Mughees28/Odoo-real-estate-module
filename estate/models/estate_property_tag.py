from odoo import fields, models


class EstatePropertiesTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)',
         'Tag name must be unique.')
    ]
