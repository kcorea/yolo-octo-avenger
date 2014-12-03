# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import json

def index():
    """ """
    part_one_url = URL('part_one')
    part_two_url = URL('part_two')
    return dict(part_one_url=part_one_url, part_two_url=part_two_url)

def increment():
    name = request.vars.msg[1:len(request.vars.msg)-1] or '' 
    president = db(db.president.name==name).select(db.president.ALL).first()
    if president is not None:
        new_master_counter = president.master_counter + 1
        new_counter = president.counter + 1
        president.update_record(counter=new_counter)
        president.update_record(master_counter=new_master_counter)
        return response.json(dict(result=new_counter))
    else:
        return response.json(dict(result=-1000))

def decrement():
    name = request.vars.msg[1:len(request.vars.msg)-1] or ''
    president = db(db.president.name==name).select(db.president.ALL).first()
    if president is not None:
        if president.counter==0: 
            new_counter = 0
        else: 
            new_counter = president.counter - 1
        if president.master_counter==0:
            new_master_counter = 0
        else:
            new_master_counter = president.master_counter - 1
        president.update_record(counter=new_counter)
        president.update_record(master_counter=new_master_counter)
        return response.json(dict(result=new_counter))

def part_one():
    # reset counters
    for president in db(db.president).select():
        president.update_record(counter=0)
    presidents = db(db.president).select()
    increment_url = URL('increment')
    decrement_url = URL('decrement')
    return dict(presidents=presidents, increment_url=increment_url,
                                       decrement_url=decrement_url)

def view_part_one():
    return dict(grid=SQLFORM.smartgrid(db.president))

def part_two():
    random_list = db(db.president).select(db.president.ALL, orderby='<random>')
    return dict(random_list=random_list)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


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
