# -*- coding: utf-8 -*-
# from odoo import http


# class EditAccountAsset(http.Controller):
#     @http.route('/edit_account_asset/edit_account_asset', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_account_asset/edit_account_asset/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_account_asset.listing', {
#             'root': '/edit_account_asset/edit_account_asset',
#             'objects': http.request.env['edit_account_asset.edit_account_asset'].search([]),
#         })

#     @http.route('/edit_account_asset/edit_account_asset/objects/<model("edit_account_asset.edit_account_asset"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_account_asset.object', {
#             'object': obj
#         })
