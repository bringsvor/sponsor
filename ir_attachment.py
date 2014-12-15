__author__ = 'tbri'

from openerp import models, fields, api, _

class ir_attachment(models.Model):
    _inherit = 'ir.attachment'
    _order = 'sequence'

    sequence = fields.Integer(string='Sequence', default=10,
        help="Gives the sequence of this line when displaying the attachment.")
    visible = fields.Boolean(string = 'Visible', default=True,
                             help='Should this image be visible in the report.')
