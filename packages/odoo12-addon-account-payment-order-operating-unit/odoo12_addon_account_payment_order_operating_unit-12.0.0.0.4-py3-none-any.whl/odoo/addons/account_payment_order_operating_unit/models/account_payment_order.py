from odoo import fields, models, api
from odoo.tools.translate import _


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    operating_unit_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_get_operating_unit_ids",
        store=False
    )

    @api.depends('payment_line_ids')
    def _get_operating_unit_ids(self):
        operating_units = {}
        vals = []
        for record in self:
            for payment_line in record.payment_line_ids:
                operating_units[
                    payment_line.operating_unit_id.id
                ] = payment_line.operating_unit_id.id
            for operating_unit_id in operating_units.keys():
                vals.append(operating_unit_id)
            record.operating_unit_ids = vals

    @api.multi
    def _create_reconcile_move(self, hashcode, blines):
        self.ensure_one()
        moves = []
        post_move = self.payment_mode_id.post_move
        mvals = self._prepare_move(blines)
        move = self.env['account.move'].create(mvals)
        blines.reconcile_payment_lines()
        if post_move:
            move.post()

    @api.multi
    def _prepare_move(self, bank_lines):
        if self.payment_type == 'outbound':
            ref = _('Payment order %s') % self.name
        else:
            ref = _('Debit order %s') % self.name
        if bank_lines and len(bank_lines) == 1:
            ref += " - " + bank_lines.name
        if self.payment_mode_id.offsetting_account == 'bank_account':
            journal_id = self.journal_id.id
        elif self.payment_mode_id.offsetting_account == 'transfer_account':
            journal_id = self.payment_mode_id.transfer_journal_id.id
        vals = {
            'journal_id': journal_id,
            'ref': ref,
            'payment_order_id': self.id,
            'line_ids': [],
        }
        partner_ml_vals_items = self._prepare_move_lines_partner_account(
            bank_lines
        )
        for partner_ml_vals_item in partner_ml_vals_items:
            vals['line_ids'].append((0, 0, partner_ml_vals_item))
        trf_ml_vals_items = self._prepare_move_lines_offsetting_account(
            bank_lines
        )
        for trf_ml_vals_item in trf_ml_vals_items:
            vals['line_ids'].append((0, 0, trf_ml_vals_item))
        return vals

    @api.multi
    def _prepare_move_lines_partner_account(self, bank_lines):
        vals_collection = []
        amount_company_currency_col = {}
        for bank_line in bank_lines:
            if self.payment_type == 'outbound':
                name = _('Payment bank line %s') % bank_line.name
            else:
                name = _('Debit bank line %s') % bank_line.name
            if bank_line.payment_line_ids[0].move_line_id:
                account_id =\
                    bank_line.payment_line_ids[0].move_line_id.account_id.id
            else:
                if self.payment_type == 'inbound':
                    account_id =\
                        bank_line.partner_id.property_account_receivable_id.id
                else:
                    account_id =\
                        bank_line.partner_id.property_account_payable_id.id
            for payment_line in bank_line.payment_line_ids:
                if bank_line.id not in amount_company_currency_col.keys():
                    amount_company_currency_col[bank_line.id] = {}
                if (
                    payment_line.operating_unit_id.id not in
                    amount_company_currency_col[bank_line.id].keys()
                ):
                    amount_company_currency_col[
                        bank_line.id
                    ][
                        payment_line.operating_unit_id.id
                    ] = {
                        'name': name,
                        'account_id': account_id
                    }
                if (
                    'amount' not in
                    amount_company_currency_col[
                        bank_line.id
                    ][
                        payment_line.operating_unit_id.id
                    ].keys()
                ):
                    amount_company_currency_col[
                        bank_line.id
                    ][
                        payment_line.operating_unit_id.id
                    ]['amount'] = payment_line.amount_company_currency
                else:
                    amount_company_currency_col[
                        bank_line.id
                    ][
                        payment_line.operating_unit_id.id
                    ]['amount'] += payment_line.amount_company_currency

        for bank_line_id in amount_company_currency_col.keys():
            bank_line = self.env['bank.payment.line'].browse(bank_line_id)
            for operating_unit_id in amount_company_currency_col[bank_line_id]:
                vals_collection.append({
                    'name': amount_company_currency_col[
                        bank_line_id
                    ][
                        operating_unit_id
                    ]['name'],
                    'bank_payment_line_id': bank_line_id,
                    'partner_id': bank_line.partner_id.id,
                    'account_id': amount_company_currency_col[
                        bank_line_id
                    ][
                        operating_unit_id
                    ]['account_id'],
                    'credit': (
                        self.payment_type == 'inbound' and
                        amount_company_currency_col[
                            bank_line_id
                        ][
                            operating_unit_id
                        ]['amount'] or 0.0
                    ),
                    'debit': (
                        self.payment_type == 'outbound' and
                        amount_company_currency_col[
                            bank_line_id
                        ][
                            operating_unit_id
                        ]['amount'] or 0.0
                    ),
                    'operating_unit_id': operating_unit_id
                })
        # TODO: Adjust multicurrency
#         if bank_line.currency_id != bank_line.company_currency_id:
#             sign = self.payment_type == 'inbound' and -1 or 1
#             vals.update({
#                 'currency_id': bank_line.currency_id.id,
#                 'amount_currency': bank_line.amount_currency * sign,
#             })
        return vals_collection

    @ api.multi
    def _prepare_move_lines_offsetting_account(self, bank_lines):
        vals_collection = []
        amount_company_currency_col = {}
#         amount_payment_currency_col = {}

        if self.payment_type == 'outbound':
            name = _('Payment order %s') % self.name
        else:
            name = _('Debit order %s') % self.name

        if self.payment_mode_id.offsetting_account == 'bank_account':
            account_id = self.journal_id.default_debit_account_id.id
        elif self.payment_mode_id.offsetting_account == 'transfer_account':
            account_id = self.payment_mode_id.transfer_account_id.id

        partner_id = False
        for index, bank_line in enumerate(bank_lines):
            if index == 0:
                partner_id = bank_line.payment_line_ids[0].partner_id.id
            elif bank_line.payment_line_ids[0].partner_id.id != partner_id:
                # we have different partners in the grouped move
                partner_id = False
                break

        for bank_line in bank_lines:
            for payment_line in bank_line.payment_line_ids:
                if (
                    payment_line.operating_unit_id.id not in
                    amount_company_currency_col.keys()
                ):
                    amount_company_currency_col[
                        payment_line.operating_unit_id.id
                    ] = payment_line.amount_company_currency
                else:
                    amount_company_currency_col[
                        payment_line.operating_unit_id.id
                    ] += payment_line.amount_company_currency

        for operating_unit_id in amount_company_currency_col.keys():
            if self.payment_mode_id.offsetting_account == 'bank_account':
                vals = {'date': bank_lines[0].date}
            else:
                vals = {'date_maturity': bank_lines[0].date}
            vals.update({
                'name': name,
                'partner_id': partner_id,
                'account_id': account_id,
                'credit': (
                    self.payment_type == 'outbound' and
                    amount_company_currency_col[operating_unit_id] or 0.0
                ),
                'debit': (
                    self.payment_type == 'inbound' and
                    amount_company_currency_col[operating_unit_id] or 0.0
                ),
                'operating_unit_id': operating_unit_id
            })
            vals_collection.append(vals)
        # TODO: Adjust multicurrency
#         if bank_lines[0].currency_id != bank_lines[0].company_currency_id:
#             sign = self.payment_type == 'outbound' and -1 or 1
#             vals.update({
#                 'currency_id': bank_lines[0].currency_id.id,
#                 'amount_currency': amount_payment_currency * sign,
#             })
        return vals_collection
