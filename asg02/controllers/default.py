@auth.requires_login()
def index():
   """ display home page  """
   # grab all tasks assigned by this user and sort them by title
   user_assigned_to = db(db.tasks.assigner==auth.user_id)
   assigned_to = user_assigned_to.select(db.tasks.ALL, orderby=db.tasks.title)

   # grab all tasks assigned to this user and sort them by title
   user = db(db.auth_user.id==auth.user_id).select().first()
   user_assigned_by = db(db.tasks.assignee_email==user.email)
   assigned_by = user_assigned_by.select(db.tasks.ALL, orderby=db.tasks.title)

   return dict(assigned_to=assigned_to, assigned_by=assigned_by)


@auth.requires_login()
def create():
   """ create a new task """
   form = SQLFORM(db.tasks)
   if form.process().accepted:
      session.flash = T('Your task has been created')
      redirect(URL('index'))
   return dict(form=form)


def show_assignee():
   """ shows a task to the assignee """
   task = db.tasks(request.args(0,cast=int))
   assigner = db(db.auth_user.id==task.assigner).select().first()
   # if user email matches task, then show o.w. raise 404
   if task.assignee_email==db.auth_user.email:
      form1 = FORM(
                INPUT(_type='radio', _name='status', 
                      _value='accepted', _checked='checked'), ' accept ',
                INPUT(_type='radio', _name='status', 
                      _value='rejected'), ' reject ',
                INPUT(_type='submit', _value='submit'))

      form2 = FORM(
                INPUT(_type='radio', _name='status', 
                      _value='completed'), ' done ',
                INPUT(_type='submit', _value='submit'))
      if form1.process().accepted:
         task.status = form1.vars.status
         task.update_record()
         redirect (URL('index'))
      if form2.process().accepted:
         task.status = form2.vars.status
         task.update_record()
         redirect (URL('index'))
      return dict(task=task, assigner=assigner, form1=form1, form2=form2)
   else:
      raise HTTP(404)


def show_assigner():
   """ shows a task to the assigner """
   task = db.tasks(request.args(0,cast=int))
   # if user assigned task, then show o.w. raise 404
   if task.assigner==auth.user_id:
      return dict(task=task)
   else:
      raise HTTP(404)


def user():
   return dict(form=auth())

