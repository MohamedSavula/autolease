# -*- coding: utf-8 -*-
# from odoo import http


# class ContractCar(http.Controller):
#     @http.route('/contract_car/contract_car', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contract_car/contract_car/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contract_car.listing', {
#             'root': '/contract_car/contract_car',
#             'objects': http.request.env['contract_car.contract_car'].search([]),
#         })

#     @http.route('/contract_car/contract_car/objects/<model("contract_car.contract_car"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contract_car.object', {
#             'object': obj
#         })
