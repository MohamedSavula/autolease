# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words



class Carlicense(models.Model):
    _name = 'car.license'
    _rec_name = 'car_num'
    _description = 'car_license'

    car_num = fields.Char(string="رقم السيارة", required=True, )
    car_type = fields.Char(string="نوع السيارة", required=True, )

    paper_inspection = fields.Float(string="ورق فحص", required=False, )
    annual_tax = fields.Float(string="ضريبة سنوية", required=False, )
    compulsory_insurance = fields.Float(string="تامين اجباري", required=False, )
    data_update_form = fields.Float(string="استمارة تحديث بيانات", required=False, )
    electronic_inspection_fees = fields.Float(string="رسوم فحص الكتروني", required=False, )
    violations_receipt_clearance = fields.Float(string="ايصال مخالفات و براءة ذمة", required=False, )
    environmental_engineer_electronic_inspection = fields.Float(string="مهندس البيئة و فحص الكتروني", required=False, )
    fingerprinting_deportation = fields.Float(string="رفع البصمة و ابعاد", required=False, )
    employee_bonus = fields.Float(string="اكرامية موظف", required=False, )
    reviewer_bonus = fields.Float(string="اكرامية مراجع", required=False, )
    computer_delivery_bonus = fields.Float(string="اكرامية الكمبيوتر و تسليم", required=False, )
    traffic_sticker_bonus = fields.Float(string="اكرامية ملصق مرور", required=False, )
    violations_stamp = fields.Float(string="دمغة مخالفات", required=False, )
    scale = fields.Float(string="ميزان", required=False, )
    fire_extinguisher_purchase = fields.Float(string="شراء طفاية", required=False, )
    treasury_acknowledgment_bonus = fields.Float(string="اكرامية خزينة التبين", required=False, )
    military_bonus = fields.Float(string="اكرامية عسكري", required=False, )
    photocopying = fields.Float(string="تصوير", required=False, )
    violations_printout = fields.Float(string="برنت مخالفات", required=False, )
    employee_bonus_2 = fields.Float(string="اكرامية موظف", required=False, )
    holder_bag_triangle = fields.Float(string="حافظة \ شنطة \مثلث", required=False, )
    chain = fields.Float(string="سلسلة", required=False, )
    rescue_card_funnel_vest = fields.Float(string="كارت انقاذ \ قمع \صديري", required=False, )
    garage = fields.Float(string="جراج", required=False, )
    driving_license_inquiry_bonus = fields.Float(string="اكرامية استعلام عن الرخص", required=False, )
    writing_on_the_car = fields.Float(string="كتابة علي السيارة", required=False, )
    total = fields.Float(string="الاجمالي", required=False, )
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True,
                                  default=lambda self: self.env.company.currency_id.id)
    total_in_ar = fields.Char(string="", required=False, )

    @api.constrains('paper_inspection',
                    'annual_tax',
                    'compulsory_insurance',
                    'data_update_form',
                    'electronic_inspection_fees',
                    'violations_receipt_clearance',
                    'environmental_engineer_electronic_inspection',
                    'fingerprinting_deportation',
                    'employee_bonus',
                    'reviewer_bonus',
                    'computer_delivery_bonus',
                    'traffic_sticker_bonus',
                    'violations_stamp',
                    'scale',
                    'fire_extinguisher_purchase',
                    'treasury_acknowledgment_bonus',
                    'military_bonus',
                    'photocopying',
                    'violations_printout',
                    'employee_bonus_2',
                    'holder_bag_triangle',
                    'chain',
                    'rescue_card_funnel_vest',
                    'garage',
                    'driving_license_inquiry_bonus',
                    'writing_on_the_car')
    def get_total(self):
        for rec in self:
            rec.total = sum([rec.paper_inspection,
                             rec.annual_tax,
                             rec.compulsory_insurance,
                             rec.data_update_form,
                             rec.electronic_inspection_fees,
                             rec.violations_receipt_clearance,
                             rec.environmental_engineer_electronic_inspection,
                             rec.fingerprinting_deportation,
                             rec.employee_bonus,
                             rec.reviewer_bonus,
                             rec.computer_delivery_bonus,
                             rec.traffic_sticker_bonus,
                             rec.violations_stamp,
                             rec.scale,
                             rec.fire_extinguisher_purchase,
                             rec.treasury_acknowledgment_bonus,
                             rec.military_bonus,
                             rec.photocopying,
                             rec.violations_printout,
                             rec.employee_bonus_2,
                             rec.holder_bag_triangle,
                             rec.chain,
                             rec.rescue_card_funnel_vest,
                             rec.garage,
                             rec.driving_license_inquiry_bonus,
                             rec.writing_on_the_car]
                            )
            rec.total_in_ar = num2words(rec.total, lang='ar').replace('-', ' ').replace(',', '') + " فقط لا غير"
