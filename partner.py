__author__ = 'tbri'

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp



class Sponsorship(models.Model):
    _name = 'sponsorship'
    _order = 'end_date desc, start_date desc'

    def _sponsored_children(self):
        return 'GEI?'

    @api.multi
    def mailing(self,field):
        for sponsorship in self:
            if sponsorship.sub_sponsor_id:
                node = sponsorship.sub_sponsor_id
            else:
                node = sponsorship.sponsor_id

            return node[field]


    @api.one
    def _get_mailing(self):
        print "MAILING"
        self.mailing_name = 'HEI'

    @api.onchange('child_ident')
    def _change_ident(self):
        print "ONCANGE", self.child_ident
        if not self.child_ident:
            return
        new_child = self.env['res.partner'].search([('child_ident', '=', self.child_ident)])
        if len(new_child)==1:
            self.sponsored_child = new_child
        else:
            return {
                'warning' : {'title' : _("Error"),
                         'message' : _("Unknown child ident %s") % self.child_ident}
            }


    start_date = fields.Date(string = 'Start of sponsorship')
    end_date = fields.Date(string = 'End of sponsorship')
    #sponsor_id = fields.Many2one('sponsor_id', string='Sponsor',
    #    ondelete='cascade', index=True)

    sponsor_id = fields.Many2one('res.partner', string = 'Sponsor', domain="[('sponsor', '=', 'True')]")
    sub_sponsor_id = fields.Many2one('res.partner', string = 'Sub Sponsor', domain="[('sub_sponsor', '=', 'True')]")
    sponsored_child = fields.Many2one('res.partner', string = 'Child', domain=[('sponsored_child', '=', 'True')])
    child_ident = fields.Char(string = 'Child IDNR', related='sponsored_child.child_ident', store=True)

    mailing_name = fields.Char(string = 'Mailing name', compute=_get_mailing)

class SubSponsor(models.Model):
    _inherit = 'res.partner'

    sub_sponsor = fields.Boolean(string = 'Sub Sponsor')
    main_sponsor = fields.Many2one('res.partner', 'Main sponsor', ondelete='restrict')

    @api.one
    def check_links(self):

        print "CHECK LINKS"
        sponsorship_sponsor = self.env['sponsorship'].search([('sponsor_id', '=', self.id)])
        sponsorship_child = self.env['sponsorship'].search([('sponsored_child', '=', self.id)])
        sponsorship_sub_sponsor = self.env['sponsorship'].search([('sub_sponsor_id', '=', self.id)])

        description = None
        if len(sponsorship_sponsor):
            description = 'a sponsor.'
        elif len(sponsorship_child):
            description = 'a sponsored child.'
        elif len(sponsorship_sub_sponsor):
            description = 'a sub sponsor.'

        print "DESCRIPTION", description
        if description:
            raise Warning(_("Partner %s cannot be deleted since it is %s") % (self.name, description))


    def unlink(self, cr, uid, ids, context=None):
        print "UNLINK"
        retval = self.check_links(cr, uid, ids, context)
        if retval:
            return retval

        return super(SubSponsor, self).unlink(cr, uid, ids, context=context)

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
    last_invoiced = fields.Date(string = 'Last invoiced', default='01-01-1900')
    # TODO Clean this up
