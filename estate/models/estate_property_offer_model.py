from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertiesOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model for Real-Estate Properties"

    price = fields.Float()

    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string='Status',
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, copy=False)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    create_date = fields.Date(default=fields.Date.context_today, invisible=True, readonly=True)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", invisible=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    @api.depends("validity", "create_date")
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def accepted(self):
        for record in self:
            property_offers = record.property_id.offer_ids
            for offer in property_offers:
                if offer.status == "accepted":
                    raise UserError("Only one offer can be accepted for a property.")

        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = self.price
            record.property_id.buyer = self.partner_id

    def refused(self):
        for record in self:
            record.status = "refused"

    _sql_constraints = [
        ('check_price', 'CHECK(price>0)',
         'Price must be a positive integer.')
    ]

    @api.constrains('selling_price')
    def check_selling_price(self):

        for record in self:
            sell = record.property_id.expected_price * 0.9

            if record.price >= sell:
                record.accepted()

            else:

                raise UserError('Selling price must be greater than 90% of expected price.')
