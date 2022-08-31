# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    analytic_account_id = fields.Many2one(related="order_id.analytic_account_id", readonly=False)
