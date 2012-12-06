# -*- coding: utf-8 -*-

def index():
    q = SQLFORM.factory(Field('service', requires=IS_IN_DB(db,'services.id', '%(service)s')))
    if q.process().accepted:
        session.q = q.vars.service
        redirect(URL('results'))
    return dict(q=q, session=session)

def results():
    grid = SQLFORM.grid(query = db.clinics.services.contains(session.q),
             deletable=False,
             editable=False,
             create=False)
    return dict(grid=grid)

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
            redirect(URL('index'))
        return dict(form=form, clinic=clinic)
    else:
        form = SQLFORM(table=db.clinics)
        if form.process().accepted:
            auth.add_permission(auth.user_id, 'canEditClinic')
            redirect(URL('index'))
    return dict(form=form, session=session)

def delete():
    clinic = db.clinics(request.args[0]) or redirect(URL('index'))
    form = SQLFORM.factory(Field('Confirm', 'boolean', default=False))
    if form.process().accepted:
        db(db.clinics.id == request.args[0]).delete()
        auth.del_permission(auth.user_id, 'canEditClinic')
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
