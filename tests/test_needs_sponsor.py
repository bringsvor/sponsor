__author__ = 'tbri'

from openerp.tests.common import TransactionCase

class TestNeedsSponsor(TransactionCase):
    def setUp(self):
        super(TestNeedsSponsor, self).setUp()
        self.partner_model = self.registry('res.partner')

    def test_sponsorship_terminated(self):
        cr, uid = self.cr, self.uid

        r = self.partner_model.create({'name' : 'child1'})
        rr = self.partner_model.browse(cr, uid, [r])
        self.assertTrue(rr.needs_sponsor)
