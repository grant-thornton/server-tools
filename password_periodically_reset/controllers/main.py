# -*- coding: utf-8 -*-
# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import werkzeug.utils

from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class AuthSignupHome(AuthSignupHome):

    @http.route()
    def web_login(self, *args, **kw):
        """Force the password reset if expired"""
        qcontext = self.get_auth_signup_qcontext()
        user = request.env["res.users"].sudo().search([
            ("login", "=", qcontext.get("login"))
        ])
        if user.partner_id.signup_valid:
            return werkzeug.utils.redirect(
                '/web/reset_password?token={0}&db={1}'.format(
                    user.partner_id.signup_token, qcontext.get('db')))
        return super(AuthSignupHome, self).web_login(*args, **kw)
