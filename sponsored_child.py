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

    sponsored_child = fields.Boolean(string = 'Sponsored Child')
    gender = fields.Selection(string = 'Gender', selection=[('male', 'Male'), ('female', 'Female')])
    school = fields.Many2one('school', 'School', ondelete='restrict')
    date_of_birth = fields.Date(string = 'Date of birth')
    school_class = fields.Char(string = 'Class in school')

    text_info_eng = fields.Text(string = 'Description (English)')
    text_info_nor = fields.Text(string = 'Description (Norwegian)')
    village = fields.Many2one('village', 'Village', ondelete='restrict')

    needs_sponsor = fields.Boolean(string = 'Needs sponsor', store=True, compute=_calc_needs_sponsor, default=True)
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
                assert partner.fields_get()[attribute]['relation'] in ('res.partner', 'village', 'school')
                current_value = partner[attribute].name
                foreign_object = self.pool.get(partner.fields_get()[attribute]['relation'])
                val = foreign_object.browse(cr, uid, int(value)).name
                body += '%s changes from %s to %s<br />\n' % (attribute_name, current_value, val)
            else:
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
