# -*- coding: utf-8 -*-
# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Password Periodically Reset",
    "version": "10.0.1.0.0",
    "category": "Extra Tools",
    "website": "https://github.com/OCA/server-tools",
    "author": "Grant Thornton S.L.P",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "auth_signup"
    ],
    "data": [
        "data/password_periodically_reset_data.xml",
        "views/res_company_view.xml",
    ],
}
