# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepositCar(models.Model):
    _name = 'deposit.car'
    _description = 'Deposit Car'

    deposit = fields.Float(string="Deposit", required=False, )
    deposit_date = fields.Date(string="Date", required=False, )
    deposit_id = fields.Many2one(comodel_name="contract.car", string="", required=False, )


class ContractCar(models.Model):
    _name = 'contract.car'
    _description = 'Contract Car'

    name = fields.Char(string="Name", default=lambda self: 'New')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    vat = fields.Char(string='Tax ID', )
    website = fields.Char('Website Link')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    email = fields.Char()
    phone = fields.Char()
    mobile = fields.Char()
    company_id = fields.Many2one('res.company', 'Company')
    # page Driving License
    driving_license_number = fields.Char(string="Driving license number", required=False, )
    release_date = fields.Date(string="Release Date", required=False, )
    issued_by = fields.Char(string="Issued by", required=False, )
    expiry_date = fields.Date(string="Expiry Date", required=False, )
    date_of_birth = fields.Date(string="Date Of Birth", required=False, )
    country_customize_id = fields.Many2one('res.country', string='Nationality')
    passport = fields.Char(string="Passport", required=False, )
    date_of_issue = fields.Date(string="Date Of Issue", required=False, )
    # Car Details
    number_of_days = fields.Integer(string="Number Of Days", required=False, )
    driver_id = fields.Many2one('res.partner', string='Driver', required=False)
    additional_driver_id = fields.Many2one('res.partner', string='Additional Driver', required=False)
    # Voucher Car
    voucher_no = fields.Char(string="Voucher NO", required=False, )
    voucher_value = fields.Float(string="Voucher Value", required=False, )
    credit_card_no = fields.Char(string="Credit Card NO", required=False, )
    type = fields.Char(string="Type", required=False, )
    approval_no = fields.Char(string="Approval NO", required=False, )
    voucher_expiry = fields.Date(string="Expiry", required=False, )
    # Cars Data
    kms_in = fields.Char(string="KMS In", required=False, )
    kos_out = fields.Char(string="KMS Out", required=False, )
    kms_driven = fields.Char(string="kMS Driven", required=False, )
    kms_allowed = fields.Char(string="kMS Allowed", required=False, )
    ex_kms = fields.Char(string="EX KMS", required=False, )
    plate_no = fields.Char(string="Plate NO", required=False, )
    model_no = fields.Char(string="Model NO", required=False, )
    engine_number = fields.Char(string="Engine Number", required=False, )
    chassis_number = fields.Char(string="Chassis Number", required=False, )
    gas_out = fields.Selection(string="Gas In",
                               selection=[('e', 'E'), ('1', '1/4'), ('2', '1/2'), ('3', '3/4'), ('f', 'F'), ],
                               required=False, )
    gas_in = fields.Selection(string="Gas Out",
                              selection=[('e', 'E'), ('1', '1/4'), ('2', '1/2'), ('3', '3/4'), ('f', 'F'), ],
                              required=False, )
    # Deposit
    deposit_ids = fields.One2many(comodel_name="deposit.car", inverse_name="deposit_id", string="", required=False, )
    # rental
    date_car_in = fields.Datetime(string="Date and Time In", required=False, )
    date_car_out = fields.Datetime(string="Date and Time Out", required=False, )
    car_days = fields.Integer(string="Days", required=False, )
    car_hours = fields.Integer(string="Ex Hours", required=False, )
    car_weeks = fields.Integer(string="Weeks AT", required=False, )
    ex_km = fields.Integer(string="EX.KM", required=False, )
    subtotal = fields.Float(string="Subtotal", required=False, )
    discount = fields.Float(string="Discount %", required=False, )
    net = fields.Float(string="Subtotal", required=False, )
    # Extras
    delivery_charge = fields.Float(string="Delivery Charge", required=False, )
    inspection_charge = fields.Float(string="Inspection Charge", required=False, )
    pai = fields.Float(string="PAI", required=False, )
    sales_tax = fields.Float(string="Sales Tax 10 %", required=False, )
    cdw = fields.Float(string="CDW", required=False, )
    refuelling = fields.Float(string="Refuelling", required=False, )
    service = fields.Float(string="Service", required=False, )
    driver_per_day = fields.Float(string="Driver Per Day", required=False, )
    additional_hours = fields.Float(string="Additional Hours", required=False, )
    net_subtotal = fields.Float(string="Subtotal", required=False, )
    plus = fields.Float(string="Plus", required=False, )
    less = fields.Float(string="Less", required=False, )
    total_charges = fields.Float(string="Total Charges", required=False, )
    less_total_deposit = fields.Float(string="Less Total Deposit", required=False, )
    net_due = fields.Float(string="Net Due", required=False, )
    refund = fields.Float(string="Net Due", required=False, )
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sales Order")

    @api.onchange('partner_id')
    def data_customer(self):
        for rec in self:
            if rec.partner_id:
                rec.vat = rec.partner_id.vat
                rec.website = rec.partner_id.website
                rec.street = rec.partner_id.street
                rec.street2 = rec.partner_id.street2
                rec.zip = rec.partner_id.zip
                rec.city = rec.partner_id.city
                rec.state_id = rec.partner_id.state_id.id
                rec.country_id = rec.partner_id.country_id.id
                rec.country_code = rec.partner_id.country_code
                rec.email = rec.partner_id.email
                rec.phone = rec.partner_id.phone
                rec.mobile = rec.partner_id.mobile
                rec.company_id = rec.partner_id.company_id.id

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('contract.car')
        return super(ContractCar, self).create(vals)

