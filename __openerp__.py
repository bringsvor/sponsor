# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Bringsvor Consulting AS and Tinderbox AS
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Sponsorship',
    'version': '1.0',
    'author': 'Bringsvor Consulting AS and Tinderbox AS',
    'website': 'http://www.bringsvopr.com',
    'category': 'Humanitarian Aid',
    'description': """
Sponsorship
===========

Module to handle sponsored children. Human Aid.
""",
    'depends': ['account', 'document', 'document_images', 'document_images_on_partner', 'report', 'web'],
    'data': [
        'security/sponsor_security.xml',
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/wizard_view.xml',
        'child_workflow.xml',
        #'views/sponsor_letter.xml',
        'views/reports.xml',
        'views/mailing_report.xml',
        'wizards/invoice_sponsorship.xml',
        'data/sponsorship_data.xml',
        'views/ir_attachment.xml',
    ],
    'demo': [],
    'test': [
        'test/sponsor_mapping.yml',
        'test/add_sponsorship_wizard.yml',
        'test/sponsor_info.yml',
        'test/child.yml',
        'test/images.yml',
        'test/needs_sponsor.yml',
    ],

    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
}

