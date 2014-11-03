import datetime

__author__ = 'tbri'

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp


class SponsoredChild(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('sponsors')
    def _calc_needs_sponsor(self):
        self.needs_sponsor = len(self.sponsors) == 0

    @api.one
    @api.depends('date_of_birth', 'birthyear')
    def _calc_age(self):
        if not self.sponsored_child:
            self.probable_age = None
            return

        now = datetime.date.today().year
        if self.date_of_birth:
            dob_year =  datetime.datetime.strptime(self.date_of_birth,'%Y-%m-%d').year
            self.probable_age = now - dob_year
        elif self.birthyear:
            self.probable_age = now - self.birthyear
        else:
            raise Warning(_('Either birthdate or birth year must be set.'))

    @api.one
    @api.depends('previous_images')
    def _get_number_of_images(self):
        number = 0
        if self.image:
            number += 1

        if not self.previous_images:
            self.number_of_images = number
        else:
            self.number_of_images = number + len(self.previous_images)

    def included_visits(self, all_visits):
        return filter(lambda visit: visit.include_in_letter, all_visits)

    def sponsor_names(self):
        retval = []
        for sponsorship in self.sponsors:
            if sponsorship.sub_sponsor_id:
                retval.append(sponsorship.sub_sponsor_id.name)
            else:
                retval.append(sponsorship.sponsor_id.name)
        return retval

    @api.one
    def _get_address(self):
        self.child_address = self.village.child_address

    child_address = fields.Char(string = _('Address'), compute=_get_address)
    sponsored_child = fields.Boolean(string = _('Child'))
    gender = fields.Selection(string = _('Gender'), selection=[('male', _('Male')), ('female', _('Female'))])
    school = fields.Many2one('school', _('School'), ondelete='restrict', track_visibility='onchange')
    date_of_birth = fields.Date(string = _('Date of birth'))
    birthyear = fields.Integer(string = _('Birthyear'))
    school_class = fields.Char(string = _('Class in school'), track_visibility='onchange')
    text_info = fields.One2many('child_info', 'sponsored_child')
    village = fields.Many2one('village', _('Village'), ondelete='restrict', track_visibility='onchange')

    probable_age = fields.Integer(string = _('Probable age'), store=True, compute=_calc_age)
    needs_sponsor = fields.Boolean(string = _('Needs sponsor'), store=True, compute=_calc_needs_sponsor, default=True)
    #sponsor_name = fields.Char(string = 'Sponsor name', compute=_get_sponsor_name)
    ####sponsorships = fields.One2many('sponsorship', 'sponsor_id', string='Sponsors')
    mother = fields.Char(string = _('Mother'), size=32)
    father = fields.Char(string = _('Father'), size=32)

    sponsors = fields.One2many('sponsorship', 'sponsored_child')
    child_ident = fields.Char(string = _('Child Code'))

    state = fields.Selection([
        ('draft',_('Draft')),
        ('active',_('Active')),
        ('inactive', _('Inactive'))],
        string=_('Status'), index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help = _("* The 'Draft' state is used when a child is just entered into the system.\n"
        "* The 'Active' state is when a child has been approved and is active.\n"
        "* The 'Inactive' state is when a child is no longer active.\n")
    )

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_validate(self):
        self.state = 'active'

    @api.one
    def action_inactive(self):
        self.state = 'inactive'


    @api.multi
    def child_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        # Create
        print "SPONSORS", self.sponsors
        print "PICS", self.image_ids
        return self.env['report'].get_action(self, 'sponsor.report_sponsorship_view')


    def Xwrite(self, cr, uid, id, vals, context=None, check=True, update_check=True):
        body = ''
        print "WRITE", vals
        partner = self.browse(cr, uid, id)
        for attribute, value in vals.items():
            if attribute == 'image':
                print "NEW IMAGE"
            current_value = partner[attribute]
            attribute_name = partner.fields_get()[attribute]['string']
            if partner.fields_get()[attribute]['type'] == 'many2one':
                assert partner.fields_get()[attribute]['relation'] in ('res.partner', 'village', 'school')
                current_value = partner[attribute].name
                foreign_object = self.pool.get(partner.fields_get()[attribute]['relation'])
                val = foreign_object.browse(cr, uid, int(value)).name
                body += '%s changes from %s to %s<br />\n' % (attribute_name, current_value, val)
            elif attribute != 'image':
                body += '%s changes from %s to %s<br />\n' % (attribute_name, current_value, value)

        result = super(SponsoredChild, self).write(cr, uid, id, vals, context, check, update_check)
        self.message_post(cr, uid, id, subject='Attribute updated', body=body, context=context)
        return result

class Village(models.Model):
    _name = 'village'


    @api.model
    # @api.returns('account.analytic.journal', lambda r: r.id)
    def _get_gambia(self):
        return self.env['res.country'].search([('code', '=', 'GM')], limit=1)

    @api.one
    def village_address(self):
        print "VILLAGE ADDRESS", self.child_address
        print "VILLAGE", self.name, self.district_name, self.country_id
        return self.child_address


    @api.one
    def _get_address(self):
        address =  "%(name)s<br/>%(district_name)s<br/>%(country_name)s" % {
            'name' : self.name,
            'district_name' : self.district_name,
            'country_name' : self.country_id.name
        }
        self.child_address = address

    name = fields.Char(string = _('Village'), required=True)
    district_name = fields.Char(string = _('District'), required=True)

    country_id = fields.Many2one('res.country', _('Country'), ondelete='restrict', default=_get_gambia, required=True)
    description = fields.Char(string = _('Village description'))
    child_address = fields.Char(string = 'Address', readonly=True, compute=_get_address)

class School(models.Model):
    _name = 'school'

    name = fields.Char(string = _('School'))
    village = fields.Many2one('village', _('Village'), ondelete='restrict')

class ChildInfo(models.Model):
    _name = 'child_info'
    _description = 'Information about a visit with the child.'
    when = fields.Char(string = _('Time of visit'))
    include_in_letter = fields.Boolean(string = _('Include in sponsor letter'), default=True)
    text_info_eng = fields.Text(string = _('Description (English)'))
    text_info_nor = fields.Text(string = _('Description (Norwegian)'))
    sponsored_child = fields.Many2one('res.partner', _('Child'), ondelete='restrict')