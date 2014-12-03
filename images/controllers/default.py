# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    """
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

@auth.requires_login()
def show():
    image = db.image(request.args(0,cast=int)) or redirect(URL('index'))
    db.post.image_id.default = image.id
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db(db.post.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

def download():
    return response.download(request, db)

def user():
    return dict(form=auth())

@auth.requires_membership('Manager')
def manage():
    grid = SQLFORM.smartgrid(db.image, linked_tables=['post'])
    return dict(grid=grid)

