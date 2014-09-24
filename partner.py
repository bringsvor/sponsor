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
    _name = 'sponsored_child'
    _inherit = ['res.partner']

    def _calc_needs_sponsor(self):
        print "DO WE NEED A SPONSOR?", self.id
        if not self.id:
            print "WELL; WE ARE BRAND NEW SO..."
            self.needs_sponsor = True
            return
        res = self.env['sponsorship'].search([('sponsored_child.id', '=', self.id)])
        print "RES", res, len(res) == 0
        self.needs_sponsor = len(res) == 0

    gender = fields.Selection(string = 'Gender', selection=[('male', 'Male'), ('female', 'Female')])
    school = fields.Char(string = "School", help='Which school')
    date_of_birth = fields.Date(string = 'Date of birth')
    school_class = fields.Char(string = 'Class in school')

    text_info_eng = fields.Text(string = 'Description (English)')
    text_info_nor = fields.Text(string = 'Description (Norwegian)')
    village_info = fields.Text(string = 'Info about the village')
    needs_sponsor = fields.Boolean(string = 'Needs sponsor', compute=_calc_needs_sponsor)
    parent_1 = fields.Char(string = 'Parent 1')
    parent_2 = fields.Char(string = 'Parent 2')

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

    def _sponsored_children(self):
        return 'GEI?'

    start_date = fields.Date(string = 'Start of sponsorship')
    end_date = fields.Date(string = 'End of sponsorship')
    sponsor_id = fields.Many2one('sponsor', string='Sponsor',
        ondelete='cascade', index=True)

    sponsored_child = fields.Many2one('sponsored_child', string = 'Sponsored Children')

class Sponsor(models.Model):
    _name = 'sponsor'
    _inherit = ['res.partner']

    #sponsor_id = fields.Many2one('res.partner', string="Sponsor")
    sponsored_children = fields.One2many('sponsorship', 'sponsor_id', string='Sponsored Children')