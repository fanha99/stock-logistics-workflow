# -*- coding: utf-8 -*-
# Copyright 2015-2016 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2016 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
# Copyright 2018 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from ..wizards.fill_date_backdating import check_date


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _action_done(self):
        # do actual processing
        result = super(StockMove, self)._action_done()
        # overwrite date field where applicable
        for move in result:
            if not move.picking_id.date_done:
                move.picking_id.write({'date_done': fields.Datetime.now()})
            else:
                check_date(move.picking_id.date_done)
                move.write({'date': move.picking_id.date_done})
                for ml in move.move_line_ids:
                    ml.write({'date': move.picking_id.date_done})
        return result
