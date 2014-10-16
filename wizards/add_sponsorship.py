__author__ = 'tbri'

from openerp import models, fields, api

class add_sponsorship_wizard(models.TransientModel):
    _name = 'add_sponsorship_wizard'


    def _get_all_children(self):
        c = []
        children =  self.env['sponsored_child'].search([])
        for n in children:
            c.append( (n.id, n.name))
        return c

    #sponsor_id = fields.Many2one('sponsor')
    ## child_id = fields.Many2one('sponsored_child', default=_get_first_child)
    child_id = fields.Selection( _get_all_children )
    start_date = fields.Date('Start date')
    end_date = fields.Date('End date')

    @api.one
    def data_save(self):
        print "DATA_SAVE 1", self._context
        """
        DATA_SAVAE! {'lang': 'en_US', 'search_disable_custom_filters': True, 'tz': False, 'uid': 1, 'active_model': 'sponsor', 'active_ids': [1], 'active_id': 1}
        """
        model = self._context['active_model']
        active_id = self._context['active_id']

        assert model == 'sponsor'
        sponsor = self.env['sponsor'].browse(active_id)
        print "DATA_SAVE 2", sponsor
        print "DATA_SAVE 3", self.child_id
        sponsorship = {'sponsor_id' : active_id,
                                         'sponsored_child' : int(self.child_id),
                                         'start_date' : self.start_date,
                                         'end_date' : self.end_date}
        print "CREATING SPONSORSHP"
        self.env['sponsorship'].create( sponsorship)
        return {'type': 'ir.actions.act_window_close'}