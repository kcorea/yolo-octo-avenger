@auth.requires_login()
def index():
   """ shows all user images and files """
   # get all rows of images belonging to user and sort them
   user_images = db(db.image.created_by==auth.user_id)
   images = user_images.select(db.image.ALL, orderby=db.image.title)

   # get all rows of files belonging to user and sort them
   user_files = db(db.files.created_by==auth.user_id)
   files = user_files.select(db.files.ALL, orderby=db.files.title)
   return dict(images=images, files=files)

import random
@auth.requires_login()
def create_image():
   """ creates a new image post """
   form = SQLFORM(db.image)
   ran = random.getrandbits(60)
   form.vars.random_id = ran
   if form.process().accepted:
      session.flash = T('Your image has been posted')
      redirect(URL('show_image', args=[ran]))
   return dict(form=form)

@auth.requires_login()
def create_file():
   """ creates a new image post """
   form = SQLFORM(db.files)
   ran = random.getrandbits(60)
   form.vars.random_id = ran
   if form.process().accepted:
      session.flash = T('Your file has been posted')
      redirect(URL('show_file', args=[ran]))
   return dict(form=form)

def show_image():
   """ shows an image """
   record = db(db.image.random_id==request.args(0,cast=int)).select()
   if record is not None:
      return dict(image=record.first())
   else:
      raise HTTP(404)

def show_file():
   """ provide link to download file """
   record = db(db.files.random_id==request.args(0,cast=int)).select()
   if record is not None:
      return dict(user_file=record.first())
   else:
      raise HTTP(404)

def download():
   return response.download(request, db)

def user():
   return dict(form=auth())
