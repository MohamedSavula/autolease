# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    contract_car_ids = fields.Many2many(comodel_name="contract.car", string="Contract Car")

    def create_contract_car(self):
        for rec in self:
            for line in rec.order_line:
                contract_car = self.env['contract.car'].create({
                    'partner_id': rec.partner_id.id,
                    'sale_order_id': rec.id,
                    'subtotal': line.price_subtotal,
                    'analytic_account_id': line.analytic_account_id.id,
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

    def _prepare_invoice_line(self, **optional_values):
        invoice_line = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        invoice_line['analytic_account_id'] = self.analytic_account_id.id
        return invoice_line
