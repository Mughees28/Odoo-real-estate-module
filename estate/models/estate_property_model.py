from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),
                                           ('east', 'East'), ('west', 'West')])

    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'),
         ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        string='State',
        required=True,
        default='new',
        copy=False
    )

    property_types_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer(compute="_compute_total")

    best_price = fields.Integer(compute="_compute_max")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends("offer_ids")
    def _compute_max(self):
        max_price = max(self.offer_ids.mapped("price"), default=0.0)
        self.best_price = max_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:

            self.garden_area = 0
            self.garden_orientation = ""

    def action_Sold(self):
        for record in self:
            if record.state == "sold":
                raise UserError('Property already sold.')

            elif record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError('A canceled property cannot be sold.')

    def action_Cancel(self):
        for record in self:
            if record.state == "canceled":
                raise UserError('Property already canceled.')

            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError('A sold property cannot be canceled.')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0)',
         'Expected price must be a positive integer.')
    ]
    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price>=0)',
         'Selling price must be a positive integer.')
    ]

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for record in self:
            sell = record.expected_price * 0.9
            for offer in record.offer_ids:
                if offer.price < sell:
                    offer.status = 'refused'
                    record.selling_price = 0.00
