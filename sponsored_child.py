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
        now = datetime.date.today().year
        if self.date_of_birth:
            dob_year =  datetime.datetime.strptime(self.date_of_birth,'%Y-%m-%d').year
            self.probable_age = now - dob_year
        elif self.birthyear:
            self.probable_age = now - self.birthyear

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

    sponsored_child = fields.Boolean(string = 'Sponsored Child')
    gender = fields.Selection(string = 'Gender', selection=[('male', 'Male'), ('female', 'Female')])
    school = fields.Many2one('school', 'eSchool', ondelete='restrict')
    date_of_birth = fields.Date(string = 'Date of birth')
    birthyear = fields.Integer(string = 'Birthyear')
    school_class = fields.Char(string = 'Class in school')

    text_info_eng = fields.Text(string = 'Description (English)')
    text_info_nor = fields.Text(string = 'Description (Norwegian)')
    village = fields.Many2one('village', 'Village', ondelete='restrict')

    probable_age = fields.Integer(string = 'Probable age', store=True, compute=_calc_age)
    needs_sponsor = fields.Boolean(string = 'Needs sponsor', store=True, compute=_calc_needs_sponsor, default=True)
    #sponsor_name = fields.Char(string = 'Sponsor name', compute=_get_sponsor_name)
    sponsorships = fields.One2many('sponsorship', 'sponsor_id', string='Sponsors')
    parent_1 = fields.Char(string = 'Parent 1')
    parent_2 = fields.Char(string = 'Parent 2')

    sponsors = fields.One2many('sponsorship', 'sponsored_child')
    previous_images = fields.One2many('child_image', 'sponsor_id', string='Previous images')
    number_of_images = fields.Integer(string = 'Number of pictures', compute=_get_number_of_images)

    @api.one
    def store_old_image(self):
        if not self.image:
            return
        child_image_env = self.env['child_image']
        child_image_env.create( {'image' : self.image,
                                 'sponsor_id' : self.id})

        print "STORE OLD IMAGE", self.previous_images, self.image



    def write(self, cr, uid, id, vals, context=None, check=True, update_check=True):
        body = ''

        partner = self.browse(cr, uid, id)
        for attribute, value in vals.items():
            if attribute == 'image':
                self.store_old_image(cr, uid, id)
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

    name = fields.Char(string = 'Village')
    district_name = fields.Char(string = 'District')

    country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    description = fields.Char(string = 'Village description')

class School(models.Model):
    _name = 'school'

    name = fields.Char(string = 'School')
    village = fields.Many2one('village', 'Village', ondelete='restrict')


class ChildImage(models.Model):
    _name = 'child_image'

    image = fields.Binary("Image",
            help="This field holds the image used as avatar for this contact")
    sponsor_id = fields.Many2one('res.partner', string = 'Sponsor')