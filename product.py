__author__ = 'tbri'

from openerp import models, fields, api, _

class product_template(models.Model):
    _inherit = 'product.template'

    sponsorship = fields.Boolean('Sponsorship')

