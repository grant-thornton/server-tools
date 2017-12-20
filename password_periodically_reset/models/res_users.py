# -*- coding: utf-8 -*-
# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from datetime import date, timedelta


from odoo import api, fields, exceptions, models, _
from odoo.addons.auth_signup.models.res_partner import now

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    last_password_change = fields.Date(
        compute='_get_last_password_change',
        store=True)

    @api.multi
    @api.depends('password')
    def _get_last_password_change(self):
        for user in self:
            user.last_password_change = fields.Date.today()

    @api.model
    def change_password(self, old_passwd, new_passwd):
        if old_passwd == new_passwd:
            raise exceptions.UserError(_(
                "New password should not be the same as old password."))
        return super(ResUsers, self).change_password(old_passwd, new_passwd)

    def check_reset_password(self):
        user = self.browse(self._uid)
        expiration_days = user.company_id.passwords_expiration_days
        today = date.today()
        expiration_date = today - timedelta(days=expiration_days)
        users_to_reset = self.search([
            ('last_password_change', '<', expiration_date)
        ])
        return users_to_reset.reset_expired_password()

    @api.multi
    def reset_expired_password(self):
        self.mapped('partner_id').signup_prepare(
            signup_type="reset", expiration=now(days=+1))
        template = self.env.ref(
            'password_periodically_reset.reset_expired_password_email')
        for user in self:
            if not user.email:
                raise exceptions.UserError(_(
                    "Cannot send email: user {} has no email address.").format(
                    user.name))
            template.with_context(lang=user.lang).send_mail(
                user.id, force_send=False, raise_exception=True)
            _logger.info(
                "Password reset email sent for user <{}> to <{}>".format(
                    user.login, user.email))
