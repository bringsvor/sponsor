#!/usr/bin/env python

from csv import DictReader
import oerplib

"""
Put 1100 children into the database
"""
#oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8099)
oerp = oerplib.OERP('localhost', protocol='xmlrpc', port=8069)

print(oerp.db.list())

user = oerp.login('admin', 'admin', 'barn8')
#user = oerp.login('admin', 'Fadder123', 'fadder1')
print(user.company_id.name)

"""

Fadderbarn nr,Reg dato,Avsluttet,Fornavn,Name,Status,Sex,Birth,Oppdatert skole juli 2012 fra Momodou,Forventet klasse 2012-13,Village,Mother,Father,
"""

"""
{'Status': '\xc3\x85pen', '': '', 'Name': 'Susso', 'Oppdatert skole juli 2012 fra Momodou': 'Talinding UBS', 'Mother': '', 'Father': '', 'Fadderbarn nr': '978', 'Sex': 'F', 'Forventet klasse 2012-13': '', 'Birth': '', 'Village': '', 'Fornavn': 'Isatou ', 'Avsluttet': '', 'Reg dato': '6/7/2011'}

"""

partner_attributes = ['child_ident', 'create_date', 'name', 'phone', 'type', 'zip', 'mother', 'father', 'birthdate']
csv_columns = [('Fadderbarn nr',), ('Reg dato',), ('Fornavn', 'Name'), None, None, None, ('Mother',), ('Father',),  ('Birth',)]
mapping = zip(csv_columns, partner_attributes)

partner_obj = oerp.get('res.partner')
#for partner in partner_obj.browse(partner_obj.search([])):
#    for attr in partner_attributes:
#        print(partner[attr]),
#    print



child = {'name' : 'Child1 Child1'}
#partner_obj.create(child)

csvfile = open('FadderBarn - Fadderbarn 14-15.csv')
csvfile.readline()


populate = {}

children = DictReader(csvfile)
for child in children:
    new_child = {}
    print "CHILD", child
    if not child['Name']:
      continue
    ident = child['Fadderbarn nr']
    res = partner_obj.search([('child_ident','=',ident)])
    # Stuff to populate after
    populate[ident] = (child['Village'],child['Sex'],
		child['Oppdatert skole juli 2012 fra Momodou'],child['Forventet klasse 2012-13'],
		child['Avsluttet']
)

    if len(res)!=0:
      print "Already exists", ident
      continue
    print mapping
    for src_attr, dst_attr in mapping:
        if src_attr == None:
            continue
	#for v in src_attr:
	#	print "SRC_ATTR", v, child[v]
        val = ' '.join( [child[x] for x in src_attr])
        print "VAL", val
        if not len(val.strip()):
            continue
        new_child[dst_attr] = val

    if new_child == {}:
        continue

    new_child['sponsored_child'] = True
    partner_obj.create(new_child)

"""

    populate[ident] = (child['Village'],child['Sex'],
                child['Oppdatert skole juli 2012 fra Momodou'],child['Forventet klasse 2012-13'])

"""

ident_id_list = partner_obj.search([('child_ident', 'in', populate.keys())])
ident_child_id = partner_obj.read(ident_id_list, ['child_ident'])
ident_to_child_id = {}
for x in ident_child_id:
	ident_to_child_id[x['child_ident']] = x['id']


s = [x['child_ident'] for x in ident_child_id]
print "IDENT ID", ident_child_id
print "SIZES", len(ident_id_list), len(populate.keys())
print "SETS", set(populate.keys()).difference(set(s))

villages = set([ x[0] for x in populate.values() ])
print "VILLAGES", villages
schools = set([ x[2] for x in populate.values() ])
print "SCHOOLS", schools

country_obj = oerp.get('res.country')
gambia = country_obj.search([('code','=','GM')])[0]
village_obj = oerp.get('village')
village_ent = {}
for village in villages:
	if village=='':
		continue
	v = village_obj.search([('name','=',village)])
	if v==[]:
		idd = village_obj.create({'name':village,
				'district_name' : 'District name',
				'country_id' : gambia})
		village_ent[village] = idd
	else:
		village_ent[village] = v[0]
school_obj = oerp.get('school')

school_ent = {}
for school in schools:
	s = school_obj.search([('name','=',school)])
	if s==[]:
		idd = school_obj.create({'name' : school})
		school_ent[school] = idd
	else:
		school_ent[school] = s[0]

# Now 
for ident, (village, sex, school, schoolclass, avsluttet) in populate.items():
	idd = ident_to_child_id[ident]
	v = s = None
	if village:
		v = village_ent[village]
	if school:
		s = school_ent[school]
	print "IDENT", ident, idd,sex, schoolclass, v,s
	if avsluttet.find('2011')!=-1 or avsluttet.find('2012')!=-1 or avsluttet.find('2014')!=-1:
		avsluttet = 'gjedna'
	state_inactive = {'gjedna' : 'inactive', '' : 'draft'}[avsluttet]


	partner_obj.write([idd], {'gender' : {'' : None, 'G' : 'male', 'F ?' : 'female', 'M' : 'male', 'F' : 'female'}[sex],
				'school_class' : schoolclass.strip(),
				'state' : state_inactive,
				'village' : v,
				'school' : s})




