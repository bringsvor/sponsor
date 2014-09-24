__author__ = 'tbri'

from openerp import models, fields, api

"""
https://www.odoo.com/forum/help-1/question/getting-an-access-error-on-act-window-62950
"""

class SponsoredChildSelect(models.TransientModel):
    _name = 'sponsored_child_select'
    _description = 'Wizard to add a sponsor'

    add_me = fields.Boolean(string = 'Add')
    child_id = fields.Many2one('sponsored_child', string = 'A child')
    add_sponsorship_id = fields.Many2one('add_sponsorship')

class AddSponsor(models.TransientModel):
    _name = 'add_sponsorship'
    _description = 'Wizard to add a sponsor'

    # Remember: view_init(self, fields_list, context
    def __init__(self, pool, cr):
        print "VIEW INIT"
        super(AddSponsor, self).__init__(pool, cr)
        #print "INITIALIZED", self.children_to_add

    @api.multi
    def _get_children(self):
        sponsorships = self.env['sponsorship'].read(['sponsored_child'])
        retval = []
        print "SPONSORSHIPS", sponsorships
        for child in self.env['sponsored_child'].search([]):
            print "WE HAVE A CHILD", child, child.id, type(child.id)
            if child.id in sponsorships:
                continue # already sponsored
            print "CREATE THE MAPP"
            scs = self.env['sponsored_child_select'].create({'child_id' : child.id, 'add_sponsorship_id' : self.id})
            retval.append((4, scs))
        print "GET CHILDREN", retval
        # NOOOOOOOOOOO return retval
        self.children_to_add = retval
        self.update({'children_to_add' : retval})
        assert len(self.children_to_add) == 3

    @api.multi
    @api.model
    def data_save(self, context=None):
        print "THE CONTEXT", context
        assert 'active_ids' in context
        active_ids = context['active_ids']
        assert len(context['active_ids']) == 1
        print "WE WANT ENV!"
        sponsor = self.env['sponsor'].browse(active_ids)
        print "SAVE THE DATA!", len(self.children_to_add), "CONTEXT", context

        for child in self.children_to_add:
            print "ADDING CHILD", child, child.add_me
            if not child.add_me:
                continue
            real_child_id = child.child_id.id
            sponsorship = self.env['sponsorship'].create({'sponsored_child' : real_child_id,
                                                          'sponsor_id' : sponsor.id})
            print "CREATED SPONSORSHIP", sponsorship
            #sponsor.sponsored_children.append( sponsorship )
            print "SAVED SPONSOR", sponsor.sponsored_children
            #sponsor.update()

    children_to_add = fields.One2many('sponsored_child_select', 'add_sponsorship_id', string='Children needing a sponsor', default=_get_children)

AddSponsor()