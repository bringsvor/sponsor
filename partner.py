__author__ = 'tbri'

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp


#TODO move this stuff out to its own subclass of res_partner. Maybe SponsoredChild...
"""
class sponsor_mapping(models.Model):
    start_date = fields.Date(string = "Start of sponsorship")
    end_date = fields.Date(string = "End of sponsorship")
    sponsor = fields.Many2one('res.partner', string='Sponsor')
    child = fields.Many2one('res.partner', string='Child')
"""
class SponsoredChild(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _calc_needs_sponsor(self):
        self.needs_sponsor = len(self.sponsors) == 0

    sponsored_child = fields.Boolean(string = 'Sponsored Child')
    gender = fields.Selection(string = 'Gender', selection=[('male', 'Male'), ('female', 'Female')])
    school = fields.Char(string = "School", help='Which school')
    date_of_birth = fields.Date(string = 'Date of birth')
    school_class = fields.Char(string = 'Class in school')

    text_info_eng = fields.Text(string = 'Description (English)')
    text_info_nor = fields.Text(string = 'Description (Norwegian)')
    village_info = fields.Text(string = 'Info about the village')
    needs_sponsor = fields.Boolean(string = 'Needs sponsor', compute=_calc_needs_sponsor)
    #sponsor_name = fields.Char(string = 'Sponsor name', compute=_get_sponsor_name)
    sponsorships = fields.One2many('sponsorship', 'sponsor_id', string='Sponsors')
    parent_1 = fields.Char(string = 'Parent 1')
    parent_2 = fields.Char(string = 'Parent 2')

    sponsors = fields.One2many('sponsorship', 'sponsored_child')

    def write(self, cr, uid, id, vals, context=None, check=True, update_check=True):
        body = ''

        partner = self.browse(cr, uid, id)
        for attribute, value in vals.items():
            current_value = partner[attribute]
            attribute_name = partner.fields_get()[attribute]['string']
            if partner.fields_get()[attribute]['type'] == 'many2one':
                assert partner.fields_get()[attribute]['relation'] == 'res.partner'
                current_value = partner[attribute].name
                foreign_object = self.pool.get(partner.fields_get()[attribute]['relation'])
                val = foreign_object.browse(cr, uid, int(value)).name
                body += '%s changes from %s to %s<br />\n' % (attribute_name, current_value, val)
            else:
                body += '%s changes from %s to %s<br />\n' % (attribute_name, current_value, value)

        result = super(SponsoredChild, self).write(cr, uid, id, vals, context, check, update_check)
        self.message_post(cr, uid, id, subject='Attribute updated', body=body, context=context)
        return result

class Sponsorship(models.Model):
    _name = 'sponsorship'
    _order = 'end_date desc, start_date desc'

    def _sponsored_children(self):
        return 'GEI?'

    start_date = fields.Date(string = 'Start of sponsorship')
    end_date = fields.Date(string = 'End of sponsorship')
    #sponsor_id = fields.Many2one('sponsor_id', string='Sponsor',
    #    ondelete='cascade', index=True)

    sponsor_id = fields.Many2one('res.partner', string = 'Sponsor')
    sponsored_child = fields.Many2one('res.partner', string = 'Child', domain=[('sponsored_child', '=', 'True')])

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
