# coding: utf8

db.define_table('clinics',
    Field('user', db.auth_user, default=auth.user_id),
    Field('name', 'string', required=True),
    Field('image', 'upload'),
    Field('email', 'string'),
    Field('phone', 'string'),
    Field('address', 'string'),
    Field('description', 'text'),
    format='%(name)s'
    )

db.clinics.user.writable = db.clinics.user.readable = False    
db.clinics.email.requires = IS_EMAIL()
db.clinics.phone.requires = IS_SLUG(maxlen=12, check=True, error_message='Must be valid phone number (of form xxx-xxx-xxxx)')
