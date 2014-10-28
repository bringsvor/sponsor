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
    'depends': ['account', 'document_images', 'document_images_on_partner'],
    'data': [
        'views/partner.xml',
        'views/wizard_view.xml',
        'child_workflow.xml',
    ],
    'demo': [],
    'test': [
        'test/sponsor_mapping.yml',
        'test/add_sponsorship_wizard.yml',
        'test/sponsor_info.yml',
        'test/child.yml',
        'test/images.yml'
    ],
    'installable': True,
    'auto_install': False,
}

