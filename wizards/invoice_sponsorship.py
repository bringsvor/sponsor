#!-.- encoding: utf-8 -.-
import datetime

__author__ = 'tbri'

from openerp import models, fields, api, _

class sponsorship_invoice(models.TransientModel):
    _name = 'sponsorship.invoice'

    @api.onchange('product_id')
    def changed_product(self):
        self.sponsorship_price = self.product_id.list_price


    product_id = fields.Many2one('product.product', domain="[('sponsorship','=', True)]", required=True)
    sponsorship_price = fields.Float('Membership price')

    @api.one
    def sponsorship_invoice(self):
        today = datetime.date.today()
        oneyear = datetime.timedelta(days = 365)
        yearback = today - oneyear
        ayearago = fields.Date.to_string(yearback)
        sponsors = self.env['res.partner'].search([('sponsor','=',True), '|',('last_invoiced','=',False), ('last_invoiced','<', ayearago)])
        for sponsor in sponsors:
            number_of_sponsorships = len([x for x in sponsor.sponsored_children if not x.end_date])
            if number_of_sponsorships==0:
                continue
            lines = []
            for sponsorship in sponsor.sponsored_children:
                if sponsorship.end_date:
                    continue

                line_text = 'Sponsorship of %s for %4d ' % \
                             (sponsorship.sponsored_child.name, today.year)

                if sponsorship.sponsored_child.school_class:
                    line_text += '(%s grade)' % sponsorship.sponsored_child.school_class

                line = {
                    'name' : line_text,
                    'product_id' : self.product_id.id,
                    'price_unit' : self.sponsorship_price,
                    'quantity' : number_of_sponsorships,
                }
                lines.append((0,0, line))

            invoice_info = {'partner_id' : sponsor.id,
                            'account_id' : sponsor.property_account_receivable.id,
                            'invoice_line' : lines,
                            'comment' : 'Takk for at du støtter vårt arbeid',
                        }
            self.env['account.invoice'].create(invoice_info)

            sponsor.last_invoiced = fields.Date.today()