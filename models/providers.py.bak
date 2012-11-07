# coding: utf8

db.define_table('clinics',
    Field('user', db.auth_user, default=auth.user_id),
    Field('name', 'string', required=True),
    Field('image', 'upload'),
    Field('email', 'string'),
    Field('phone', 'string'),
    Field('address', 'string'),
    Field('description', 'text'),
    Field('services', 'reference services'),
    format='%(name)s'
    )

db.define_table('service',
    Field('thing', 'string'),
    format='%(name)s'
)

db.define_table('services',
    Field('user', db.clinics),
    Field('service', db.service),
    )

db.clinics.user.writable = db.clinics.user.readable = False    
db.clinics.email.requires = IS_EMAIL()
db.clinics.phone.requires = IS_MATCH('\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
