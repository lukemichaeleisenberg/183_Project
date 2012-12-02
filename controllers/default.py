# -*- coding: utf-8 -*-

def index():
    query = SQLFORM.factory(Field('Service', requires = IS_IN_SET(['STI_Testing', 'Emergency_Medical_Services'], error_message='Requires a selection.')))
    if query.process().accepted:
        session.query = query.vars.Service
        redirect(URL('results'))
    return dict(query=query)

def results():
    query = session.query == True
    results = db.services(query)
    return dict(results=results)

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
        clinic = db.clinics(db.auth_user.clinic).select()
        form = SQLFORM(table=db.clinics, record=clinic)
        return dict(form=form)
    else:
        form = SQLFORM.factory(
        Field('Organization', requires=IS_NOT_EMPTY(error_message='requires a value')),
        Field('Address', 'string'),
        Field('City', 'string'),
        Field('Zip', 'string'),
        Field('Phone'),
        Field('Email', 'string', requires=IS_EMAIL(error_message='must be a valid email')),
        Field('Description', 'text'),
        )
        if form.process().accepted:
            session.org = form.vars.Organization
            session.address = form.vars.Address
            session.city = form.vars.City
            session.zip = form.vars.Zip
            session.phone = form.vars.Phone
            session.email = form.vars.email
            session.description = form.vars.Description
            session.clinicid = form.vars.id
            redirect(URL('editservices'))
    return dict(form=form, session=session)
    
def delete_clinic():
    crud.delete(db.services, db.auth_user.services)
    auth.del_permission(auth.user_id, 'canEditClinic')
    auth.del_permission(auth.user_id, 'canEditServices')
    return dict()

@auth.requires_login() 
def editservices():
    if auth.has_permission('canEditServices', user_id=auth.user_id):
        row = db.clinics[auth_user.clinic]
        form = crud.update(db.clinics, row, deletable=False)
        return form
    else:
        form = SQLFORM.factory(
        Field('STI_Testing', 'boolean'),
        Field('Emergency_Medical_Services', 'boolean')
        )
        if form.process().accepted:
            db.clinics.insert(
            organization = session.org, 
            street_address = session.address,
            city = session.city,
            zip = session.zip,
            phone = session.phone,
            email = session.email,
            description = session.description
            )
            db.services.insert(
            STI_Testing = form.vars.STI_Testing,
            Emergency_Medical_Services = form.vars.Emergency_Medical_Services,
            clinic = session.clinicid
            )
            user = db(db.auth_user.id==auth.user_id).select().first()
            user.update_record(clinic=session.clinicid, services=form.vars.id)
            auth.add_permission(auth.user_id, 'canEditClinic')
            auth.add_permission(auth.user_id, 'canEditServices')
            redirect(URL('index'))
    return dict(form=form, session=session)

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
