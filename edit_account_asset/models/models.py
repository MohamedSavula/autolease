# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BrandCar(models.Model):
    _name = 'brand.car'
    _description = 'Brand Car'

    name = fields.Char()


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    brand_car_id = fields.Many2one(comodel_name="brand.car", string="Brand", required=False, )
    color = fields.Char(string="Color", required=False, )
    plate = fields.Char(string="Plate#", required=False, )
    asset = fields.Char(string="Asset#", required=False, )


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    days = fields.Integer(string="Days", required=False, )
