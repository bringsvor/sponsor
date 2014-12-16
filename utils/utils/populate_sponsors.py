#!/usr/bin/env python
#-.- coding: utf-8 -.-

from csv import DictReader
import oerplib

"""
Put 371 sponsors into the database
"""
#oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8099)
oerp = oerplib.OERP('localhost', protocol='xmlrpc', port=8069)
user = oerp.login('admin', 'admin', 'barn8')
#user = oerp.login('admin', 'Fadder123', 'fadder1')
print(user.company_id.name)


csvfile = open('Faddere - Faddere imp.csv')
#csvfile.readline()
"""
}
{'Town': '1362 KOLS\xc3\x85S', 'Telephone': '', '\xc3\x85se Britt T\xc3\xb8rrestad': 'Tore Bj\xc3\xb8rn Ausland', 'Address': 'Kremlegrenda 15', 'E-mail Fadder': '', 'Kommentar': ''}
"""

populate = {}

sponsors = DictReader(csvfile)
partner_obj = oerp.get('res.partner')
country_obj = oerp.get('res.country')
norway = country_obj.search([('code','=','NO')])[0]
for sponsor in sponsors:
	name = sponsor['Åse Britt Tørrestad']
	zipcode = sponsor['Town'][:4]
	city = sponsor['Town'][5:]
	phone = sponsor['Telephone']
	address = sponsor['Address']
	email = sponsor['E-mail Fadder']

	print '%s|%s|%s|%s|%s|%s' % (name, zipcode, city, phone, address, email)
	exists = partner_obj.search([('name','=',name)])
	if exists==[]:
		partner_obj.create({'sponsor' : True,
				'name' : name.strip(),
				'zip' : zipcode,
				'city' : city,
				'phone' : phone.strip(),
				'street' : address.strip(),
				'email' : email.strip(),
				'country_id' : norway})

