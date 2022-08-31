# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

    def _prepare_invoice_line(self, **optional_values):
        invoice_line = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        invoice_line['analytic_account_id'] = self.analytic_account_id.id
        return invoice_line
