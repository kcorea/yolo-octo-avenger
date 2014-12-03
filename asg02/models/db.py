db =DAL("sqlite://storage.sqlite")

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)

db.define_table('tasks',
   Field('title'),
   Field('description', 'text'), 
   Field('assigner', 'reference auth_user', default=auth.user_id),
   Field('assignee_email'),
   Field('status', default='pending'),
   Field('created_on', 'datetime', default=request.now),
   format = '%(titles)s')

db.tasks.title.requires = IS_NOT_EMPTY()
db.tasks.description.requires = IS_NOT_EMPTY()
db.tasks.assigner.readable = db.tasks.assigner.writable = False

db.tasks.assignee_email.requires = IS_EMAIL()
db.tasks.assignee_email.requires = IS_IN_DB(db, db.auth_user.email)
db.tasks.status.readable = db.tasks.status.writable = False
db.tasks.created_on.writable = False

