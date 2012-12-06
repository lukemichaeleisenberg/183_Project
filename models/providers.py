# coding: utf8

db.define_table('clinics',
    Field('user', db.auth_user, default=auth.user_id),
    Field('organization', 'string', required=True),
    Field('street_address', 'string'),
    Field('city', 'string'),
    Field('zip', 'string'),
    Field('email', 'string'),
    Field('phone', 'string'),
    Field('services','list:reference services'),
    Field('days_hours', 'text'),
    Field('description', 'text'),
    format='%(organization)s'
    )

db.define_table('services',
    Field('service'),
    format='%(service)s'
    )

db.clinics.user.writable = db.clinics.user.readable = False
db.clinics.id.writable = db.clinics.id.readable = False
db.clinics.email.requires = IS_EMAIL()
db.clinics.services.requires = IS_IN_DB(db,'services.id', '%(service)s', multiple=True)
