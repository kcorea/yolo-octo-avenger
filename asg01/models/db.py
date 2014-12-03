db = DAL("sqlite://storage.sqlite")

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)

db.define_table('image',
   Field('title'),
   Field('filename', 'upload'),
   Field('description'),
   Field('random_id', 'integer'),
   Field('created_by', 'reference auth_user', default=auth.user_id),
   format = '%(title)s')

db.define_table('files',
   Field('title'),
   Field('filename', 'upload'),
   Field('description'),
   Field('random_id', 'integer'),
   Field('created_by', 'reference auth_user', default=auth.user_id),
   format = '%(title)s')

db.image.title.requires = IS_NOT_EMPTY()
db.image.filename.requires = IS_IMAGE()
db.image.created_by.readable = db.image.created_by.writable = False
db.image.random_id.readable = db.image.random_id.writable = False
db.image.random_id.requires = IS_NOT_IN_DB(db, db.image.random_id)

db.files.title.requires = IS_NOT_EMPTY()
db.files.created_by.readable = db.files.created_by.writable = False
db.files.random_id.readable = db.files.random_id.writable = False
db.files.random_id.requires = IS_NOT_IN_DB(db, db.files.random_id)


