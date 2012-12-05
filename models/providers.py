# coding: utf8

db.define_table('clinics',
    Field('user', db.auth_user, default=auth.user_id),
    Field('organization', 'string', required=True),
    Field('street_address', 'string'),
    Field('city', 'string'),
    Field('zip', 'string'),
    Field('email', 'string'),
    Field('phone', 'string'),
    Field('days_hours', 'text'),
    Field('description', 'text'),
    format='%(organization)s'
    )

db.define_table('services',
    Field('STI_Testing', 'boolean'),
    Field('Emergency_Medical_Services', 'boolean'),
    Field('clinic', 'reference clinics'),
    )
<<<<<<< HEAD
<<<<<<< HEAD
=======
    
=======

>>>>>>> 84a73b9... Changed to a many to many relationship
db.define_table('offers',
    Field('service_id', db.services),
    Field('clinic_id', db.clinics),
    )
>>>>>>> parent of 84a73b9... Changed to a many to many relationship

db.clinics.user.writable = db.clinics.user.readable = False
db.clinics.id.writable = db.clinics.id.readable = False
