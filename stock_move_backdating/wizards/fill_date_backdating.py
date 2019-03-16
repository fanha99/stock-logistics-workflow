# -*- coding: utf-8 -*-
# Copyright 2018 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError

def check_date(date):
    now = fields.Datetime.now()
    if date and date > now:
        raise UserError(
            "You can not process an actual "
            "movement date in the future.")

class FillDateBackdating(models.TransientModel):
    _name = "fill.date.backdating"

    date_backdating = fields.Datetime(string='Actual Movement Date')

    @api.onchange('date_backdating')
    def onchange_date_backdating(self):
        check_date(self.date_backdating)

    @api.multi
    def fill_date_backdating(self):
        """ Fill the Actual Movement Date on all pack operations. """
        self.ensure_one()
        picking = self.env['stock.picking'].browse(self._context['active_id'])
        picking.write({'date_done': self.date_backdating})
        return {'type': 'ir.actions.act_window_close'}
