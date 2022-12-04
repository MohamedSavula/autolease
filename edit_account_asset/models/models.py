# -*- coding: utf-8 -*-

from odoo import models, fields


class BrandCar(models.Model):
    _name = "brand.car"
    _description = "Brand Car"

    name = fields.Char(string="name")


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    brand_car_id = fields.Many2one(
        comodel_name="brand.car",
        string="Brand",
        required=False,
    )
    color = fields.Char(
        string="Color",
        required=False,
    )
    plate = fields.Char(
        string="Plate#",
        required=False,
    )
    asset = fields.Char(
        string="Asset#",
        required=False,
    )


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    days = fields.Integer(
        string="Days",
        required=False,
    )


class AccountAssetInherit(models.Model):
    _inherit = "account.asset"

    engine_no = fields.Char(string="Engine NO")
    chassis_no = fields.Char(string="Chassis NO")
    plate_no = fields.Char(string="Plate NO")
    model_no = fields.Char(string="Model NO")
    Car_color = fields.Char(string="Car Color")
    insurance_policy_no = fields.Char(string="Insurance Policy NO")
    rent_amount = fields.Float(string="Rent Amount")
    license_date = fields.Date(string="License Date")
    branch_id = fields.Char(string="Branch")
    vendor_id = fields.Char(string="Vendor")
    bank_and_check_no = fields.Char(string="Bank and Check NO")
    invoice_no = fields.Char(string="Invoice NO")
