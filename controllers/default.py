# -*- coding: utf-8 -*-

def index():
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    query = SQLFORM.factory(Field('Service', requires = IS_IN_SET(['STI_Testing', 'Emergency_Medical_Services'], error_message='Requires a selection.')))
    if query.process().accepted:
        session.query = query.vars.Service
        redirect(URL('results'))
    return dict(query=query, session=session)

def results():
    query = session.query == True
    results = db.services(query)
    return dict(results=results)
=======
    service_names = db(db.services.ALL).select(db.services.service).as_list()
=======
    service_names = db().select(db.services.service).as_list()
>>>>>>> 84a73b9... Changed to a many to many relationship
    service_names_list = [x['service'] for x in service_names]
    q = SQLFORM.factory(Field('service', requires=IS_IN_SET(service_names_list)))
    if q.process().accepted:
        session.q = q
        redirect(URL('results'))
    return dict(q=q, session=session)

def results():
<<<<<<< HEAD
    c = db((db.services.service == session.query) & (db.offers.service_id == db.services.id) & (db.offers.clinic_id == db.clinics.id)).select()
    return dict(results=c)
>>>>>>> parent of 84a73b9... Changed to a many to many relationship
=======
    results = db((db.services.service == session.q)).select()
    return dict(results=results)
>>>>>>> 84a73b9... Changed to a many to many relationship
=======
    service_names = db().select(db.services.service).as_list()
    service_names_list = [x['service'] for x in service_names]
    q = SQLFORM.factory(Field('service', requires=IS_IN_SET(service_names_list)))
    if q.process().accepted:
        session.q = q
        redirect(URL('results'))
    return dict(q=q, session=session)

def results():
    results = db((db.services.service == session.q)).select()
    return dict(results=results)
>>>>>>> 84a73b9... Changed to a many to many relationship

def view():
    clinic = db.clinics(request.args[0]) or redirect(URL('index'))
    return dict(clinic=clinic)

def providers():
    return dict()

@auth.requires_login()
@auth.requires_permission('isAdmin')
def manage():
    grid = SQLFORM.grid(db.clinics)
    return locals()

def providers():
    return dict()

@auth.requires_login()
def edit():
    if auth.has_permission('canEditClinic', user_id=auth.user_id):
        clinic = db.clinics(auth.user_id==db.clinics.user)
        form = SQLFORM(table=db.clinics, record=clinic)
        if form.process().accepted:
            redirect(URL('editservices'))
        return dict(form=form, clinic=clinic)
    else:
        form = SQLFORM.factory(
        Field('organization', requires=IS_NOT_EMPTY(error_message='requires a value')),
        Field('address', 'string'),
        Field('city', 'string'),
        Field('zip', 'string'),
        Field('phone'),
        Field('email', 'string', requires=IS_EMAIL(error_message='must be a valid email')),
        Field('days_and_hours', 'text'),
        Field('description', 'text'),
        )
        if form.process().accepted:
            session.org = form.vars.organization
            session.address = form.vars.address
            session.city = form.vars.city
            session.zip = form.vars.zip
            session.phone = form.vars.phone
            session.email = form.vars.email
            session.description = form.vars.description
            session.clinicid = form.vars.id
            session.days_hours = form.vars.days_and_hours
            redirect(URL('editservices'))
    return dict(form=form, session=session)

@auth.requires_login()
def editservices():
    if auth.has_permission('canEditServices', user_id=auth.user_id):
        redirect(URL('index'))
        return dict(form=form)
    else:
        form = SQLFORM.factory(
        Field('sti_testing', 'boolean'),
        Field('emergency_medical_services', 'boolean')
        )
        if form.process().accepted:
            db.clinics.insert(
            organization = session.org,
            street_address = session.address,
            city = session.city,
            zip = session.zip,
            phone = session.phone,
            email = session.email,
            days_hours = session.days_hours,
            description = session.description
            )
            if (form.vars.sti_testing):
                db.offers.insert(
                    service_id = '8',
                    clinic_id = session.clinicid
                )
            elif (form.vars.emergency_medical_services):
                db.offers.insert(
                    service_id = '9',
                    clinic_id = session.clinicid
                )
            auth.add_permission(auth.user_id, 'canEditClinic')
            auth.add_permission(auth.user_id, 'canEditServices')
            redirect(URL('index'))
    return dict(form=form, session=session)
    
def delete():
    clinic = db.clinics(request.args[0]) or redirect(URL('index'))
    form = SQLFORM.factory(Field('Confirm', 'boolean', default=False))
    if form.process().accepted:
        db(db.clinics.id == request.args[0]).delete()
        db(db.offers.id == request.args[0]).delete()
        auth.del_permission(auth.user_id, 'canEditClinic')
        auth.del_permission(auth.user_id, 'canEditServices')
        db.commit()
        session.flash = T('Your clinic has been deleted')
        redirect(URL('index'))
    return dict(form=form, user=auth.user)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
