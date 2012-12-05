# coding: utf8

db.define_table('clinics',
    Field('user', db.auth_user, default=auth.user_id),
    Field('organization', 'string', required=True),
    Field('street_address', 'string'),
    Field('city', 'string'),
    Field('zip', 'string'),
    Field('email', 'string'),
    Field('phone', 'string'),
    Field('hours_days', 'text'),
    Field('description', 'text'),
    format='%(name)s'
    )

db.define_table('services',
    Field('STI_Testing', 'boolean'),
    Field('Emergency_Medical_Services', 'boolean'),
    Field('clinic', 'reference clinics'),
    )

db.clinics.user.writable = db.clinics.user.readable = False 
db.clinics.id.writable = False
db.clinics.email.requires = IS_EMAIL()
db.clinics.phone.requires = IS_MATCH('\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
