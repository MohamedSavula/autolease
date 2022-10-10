# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class AccountAnalyticGroupInherit(models.Model):
    _inherit = 'account.analytic.group'

    rent_amount = fields.Float(string="Rent Amount", required=False, )


class AccountAnalyticAccountInherit(models.Model):
    _inherit = 'account.analytic.account'

    engine_number = fields.Char(string="Engine Number", required=False, )
    chassis_number = fields.Char(string="Chassis Number", required=False, )
    plate_no = fields.Char(string="Plate No", required=False, )
    model_number = fields.Char(string="Model Number", required=False, )
    rent_amount = fields.Float(string="Rent Amount")
    license_date = fields.Date(string="License Date", required=False, )


class AnalyticGroup(models.Model):
    _name = 'analytic.group'
    _description = 'Analytic Group'

    sales_order_id = fields.Many2one(comodel_name="sale.order")
    account_move_id = fields.Many2one(comodel_name="account.move")
    groups_analytic_id = fields.Many2one(comodel_name="account.analytic.group", string="Analytic Group", required=True)
    car_numbers = fields.Integer(string="Car Numbers")
    days = fields.Integer(string="Days")
    rent_days = fields.Integer(string="Rent Days")
    rental_value = fields.Float(string="Rental value")
    subtotal = fields.Float(string="Subtotal", compute="get_subtotal")
    tax_ids = fields.Many2many(comodel_name='account.tax', string="Taxes")
    amount_tax = fields.Float(compute="get_subtotal", store=True)
    sale_order_line_ids = fields.Many2many(comodel_name="sale.order.line")
    account_move_line_ids = fields.Many2many(comodel_name="account.move.line")

    @api.depends('car_numbers', 'rental_value')
    def get_subtotal(self):
        for rec in self:
            rec.subtotal = rec.car_numbers * rec.rental_value
            for tax in rec.tax_ids:
                rec.amount_tax = tax.amount * rec.subtotal / 100

    def unlink(self):
        for rec in self:
            account_move_id = rec.account_move_id
            if rec.sale_order_line_ids:
                rec.sale_order_line_ids.unlink()
                res = super(AnalyticGroup, self).unlink()
            elif rec.account_move_line_ids:
                rec.account_move_line_ids.unlink()
                res = super(AnalyticGroup, self).unlink()
                account_move_id._onchange_invoice_line_ids()
                account_move_id._recompute_tax_lines()
        return res


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    analytic_group_ids = fields.One2many(comodel_name="analytic.group", inverse_name="account_move_id")
    total_subtotal = fields.Float(string="Total", compute="get_total_with_tax", store=True)
    amount_tax_customize = fields.Float(string="Total", compute="get_total_with_tax", store=True)
    total_subtotal_with = fields.Float(string="Total With Tax", compute="get_total_with_tax", store=True)
    amount_to_text_customize = fields.Char(string="", required=False, compute="get_amount_to_text")
    rental_period = fields.Date()
    count_days = fields.Char(compute="get_count_days")
    date_start = fields.Date(string='Start Date')
    date = fields.Date(string='Expiration Date', index=True, tracking=True)

    @api.depends('date_start', 'date')
    def get_count_days(self):
        for rec in self:
            if rec.date_start and rec.date:
                d1 = datetime.strptime(str(rec.date_start), "%Y-%m-%d")
                d2 = datetime.strptime(str(rec.date), "%Y-%m-%d")
                rec.count_days = str(abs((d2 - d1).days))
            else:
                rec.count_days = ''

    @api.depends('total_subtotal_with')
    def get_amount_to_text(self):
        for rec in self:
            rec.amount_to_text_customize = rec.currency_id.amount_to_text(rec.total_subtotal_with).replace('and',
                                                                                                           'و') + " فقط لا غير"

    @api.depends('analytic_group_ids')
    def get_total_with_tax(self):
        for rec in self:
            rec.total_subtotal = sum(list(rec.analytic_group_ids.mapped('subtotal')))
            rec.amount_tax_customize = sum(list(rec.analytic_group_ids.mapped('amount_tax')))
            rec.total_subtotal_with = rec.total_subtotal + rec.amount_tax_customize

    def get_analytic_group_lines(self):
        for rec in self:
            rec.analytic_group_ids = False
            for group in set(rec.invoice_line_ids.mapped('groups_analytic_id')):
                for rental_value in set(
                        rec.invoice_line_ids.filtered(lambda l: l.groups_analytic_id == group).mapped('rent_amount')):
                    for rent_days in set(rec.invoice_line_ids.filtered(
                            lambda l: l.groups_analytic_id == group and l.rent_amount == rental_value).mapped(
                        'rent_days')):
                        liens = rec.invoice_line_ids.filtered(lambda
                                                                  l: l.groups_analytic_id == group and l.rent_amount == rental_value and l.rent_days == rent_days)
                        if liens:
                            rec.analytic_group_ids = [(0, 0, {
                                'groups_analytic_id': group.id,
                                'rental_value': liens[0].price_unit,
                                'rent_days': rent_days,
                                'car_numbers': sum(list(liens.mapped('quantity'))),
                                'account_move_line_ids': liens.ids,
                                'tax_ids': liens[0].tax_ids.ids,
                            })]


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    groups_analytic_id = fields.Many2one(related="analytic_account_id.group_id", store=True)
    rent_amount = fields.Float(string="Rent Amount")
    rent_days = fields.Integer(string="Rent Days", default=30)

    @api.constrains('analytic_account_id', 'quantity', 'days')
    def analytic_account_constrains(self):
        for rec in self:
            rec.move_id.get_analytic_group_lines()


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    contract_car_ids = fields.Many2many(comodel_name="contract.car", string="Contract Car")
    date_and_time_in = fields.Datetime(string="Date and time in", required=False, )
    analytic_group_ids = fields.One2many(comodel_name="analytic.group", inverse_name="sales_order_id")

    def get_analytic_group_lines(self):
        for rec in self:
            rec.analytic_group_ids = False
            for group in set(rec.order_line.mapped('groups_analytic_id')):
                for rental_value in set(
                        rec.order_line.filtered(lambda l: l.groups_analytic_id == group).mapped('rent_amount')):
                    for rent_days in set(rec.order_line.filtered(
                            lambda l: l.groups_analytic_id == group and l.rent_amount == rental_value).mapped(
                        'rent_days')):
                        liens = rec.order_line.filtered(lambda
                                                            l: l.groups_analytic_id == group and l.rent_amount == rental_value and l.rent_days == rent_days)
                        if liens:
                            rec.analytic_group_ids = [(0, 0, {
                                'groups_analytic_id': group.id,
                                'rental_value': liens[0].price_unit,
                                'rent_days': rent_days,
                                'car_numbers': sum(list(liens.mapped('product_uom_qty'))),
                                'sale_order_line_ids': liens.ids,
                            })]

    def create_contract_car(self):
        for rec in self:
            for line in rec.order_line:
                contract_car = self.env['contract.car'].create({
                    'partner_id': rec.partner_id.id,
                    'date_car_in': rec.date_and_time_in,
                    'date_car_out': rec.date_order,
                    'sale_order_id': rec.id,
                    'analytic_account_id': line.analytic_account_id.id,
                    'plate_no': line.plate_no,
                    'model_no': line.model_number,
                    'engine_number': line.engine_number,
                    'chassis_number': line.chassis_number,
                })
                contract_car.data_customer()
                rec.contract_car_ids = [(4, contract_car.id, 0)]

    def show_contract_car(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Contract Car',
                'res_model': 'contract.car',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', rec.contract_car_ids.ids)],
            }


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    engine_number = fields.Char(string="Engine Number", required=False, )
    chassis_number = fields.Char(string="Chassis Number", required=False, )
    plate_no = fields.Char(string="Plate No", required=False, )
    model_number = fields.Char(string="Model Number", required=False, )
    license_date = fields.Date(string="License Date", required=False, )
    rent_amount = fields.Float(string="Rent Amount")
    rent_days = fields.Integer(string="Rent Days", default=30)
    groups_analytic_id = fields.Many2one(related="analytic_account_id.group_id", store=True)

    @api.constrains('analytic_account_id', 'product_uom_qty')
    def analytic_account_constrains(self):
        for rec in self:
            rec.order_id.get_analytic_group_lines()

    @api.onchange('analytic_account_id')
    def get_date_analytic_account(self):
        for rec in self:
            rec.engine_number = rec.analytic_account_id.engine_number
            rec.chassis_number = rec.analytic_account_id.chassis_number
            rec.plate_no = rec.analytic_account_id.plate_no
            rec.model_number = rec.analytic_account_id.model_number
            rec.license_date = rec.analytic_account_id.license_date
            rec.rent_amount = rec.analytic_account_id.rent_amount

    @api.onchange('product_uom', 'product_uom_qty', 'analytic_account_id', 'rent_amount', 'rent_days')
    def product_uom_change(self):
        res = super(SaleOrderLineInherit, self).product_uom_change()
        self.price_unit = self.rent_amount * (self.rent_days / 30) * self.product_uom_qty
        return res

    def _prepare_invoice_line(self, **optional_values):
        invoice_line = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        invoice_line['analytic_account_id'] = self.analytic_account_id.id
        invoice_line['rent_amount'] = self.rent_amount
        invoice_line['rent_days'] = self.rent_days
        return invoice_line
