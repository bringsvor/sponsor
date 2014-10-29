__author__ = 'tbri'

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp



class Sponsorship(models.Model):
    _name = 'sponsorship'
    _order = 'end_date desc, start_date desc'

    def _sponsored_children(self):
        return 'GEI?'

    start_date = fields.Date(string = 'Start of sponsorship')
    end_date = fields.Date(string = 'End of sponsorship')
    #sponsor_id = fields.Many2one('sponsor_id', string='Sponsor',
    #    ondelete='cascade', index=True)

    sponsor_id = fields.Many2one('res.partner', string = 'Sponsor', domain="[('sponsor', '=', 'True')]")
    sub_sponsor_id = fields.Many2one('res.partner', string = 'Sub Sponsor', domain="[('sub_sponsor', '=', 'True')]")
    sponsored_child = fields.Many2one('res.partner', string = 'Child', domain=[('sponsored_child', '=', 'True')])


class SubSponsor(models.Model):
    _inherit = 'res.partner'

    sub_sponsor = fields.Boolean(string = 'Sub Sponsor')
    main_sponsor = fields.Many2one('res.partner', 'Main sponsor', ondelete='restrict')


class Sponsor(models.Model):
    #_name = 'sponsor'
    _inherit = 'res.partner'

    def _has_mailing_address(self):
        #self.mailing_address = len(self.child_ids)>0
        self.mailing_address = True # show it

    @api.one
    def _get_mailing_country(self):
        if len(self.child_ids) == 0:
            mailing = None
        else:
            mailing = self.child_ids[0]
        self.mailing_street = mailing and mailing.street or ''
        self.mailing_street2 = mailing and mailing.street2 or ''
        self.mailing_city = mailing and mailing.city or ''
        self.mailing_state_id = mailing and mailing.state_id or ''
        self.mailing_zip = mailing and mailing.zip or ''
        self.mailing_country_id = mailing and mailing.country_id or ''

    @api.one
    def _set_mailing_street(self):
        if len(self.child_ids) == 0:
            print "MAKE A CHILD"
            o = self.env['res.partner']
            print "O", o
            #child = o.create({'name' : 'hei'})
            #print "CHILD ID", child
            #self.child_ids.append(child)

        for field in ('mailing_street', 'mailing_street2', 'mailing_city', 'mailing_state_id', 'mailing_zip', 'mailing_country_id'):
            print "VERDI", field, self[field]

    #sponsor_id = fields.One2many('sponsorship', 'sponsor_id', string="Sponsor")
    sponsored_children = fields.One2many('sponsorship', 'sponsor_id', string='Sponsored Children')
    sponsor_info = fields.Html(string = 'Information')
    sponsor = fields.Boolean(string = 'Sponsor')
    mailing_name = fields.Char('Mailing name')
    mailing_address = fields.Boolean(string = 'Separate mailing address')
    mailing_street  = fields.Char('Mailing Street')
    mailing_street2  = fields.Char('Mailing Street2')
    mailing_city  = fields.Char('Mailing City')
    mailing_state_id  = fields.Many2one('res.country.state', ondelete='restrict')
    mailing_zip = fields.Char('Mailing Zip', size=24, change_default=True)
    mailing_country_id = fields.Many2one('res.country', 'Mailing country', ondelete='restrict')

    # TODO Clean this up
