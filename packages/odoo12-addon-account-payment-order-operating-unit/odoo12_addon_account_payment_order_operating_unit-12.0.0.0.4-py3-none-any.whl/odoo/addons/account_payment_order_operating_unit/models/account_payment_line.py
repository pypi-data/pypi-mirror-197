
from odoo import models, fields, api


class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_get_operating_unit_id",
        store=True
    )

    @api.depends('move_line_id')
    def _get_operating_unit_id(self):
        for record in self:
            if record.move_line_id:
                record.operating_unit_id = \
                    record.move_line_id.operating_unit_id
