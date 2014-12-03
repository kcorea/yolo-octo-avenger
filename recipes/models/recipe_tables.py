
message = "enter ingredients separated by a line, use exact measurements"
db.define_table('recipe',
   Field('title'),
   Field('description'),
   Field('image', 'upload'),
   # there will be a 1-1 correspondence between the following two fields
   Field('ingredient_list', 'list:string'),
   Field('ingredient_desc_list', 'list:string'),
   Field('ingredients', 'text', default=message),
   Field('instructions', 'text'),
   Field('hits', 'integer', default=0),
   Field('rating', 'double', default=0),
   Field('created_on', 'datetime', default=request.now),
   Field('created_by', 'reference auth_user', default=auth.user_id),
   format='%(title)s'
)

db.recipe.title.requires = IS_NOT_EMPTY()
db.recipe.description.requires = IS_NOT_EMPTY()
db.recipe.image.requires = IS_IMAGE()
db.recipe.ingredient_list.requires = IS_NOT_EMPTY()
db.recipe.ingredients.requires = IS_NOT_EMPTY()
db.recipe.instructions.requires = IS_NOT_EMPTY()

db.recipe.hits.readable = db.recipe.hits.writable = False
db.recipe.ingredient_desc_list.readable = False
db.recipe.ingredient_desc_list.writable = False
db.recipe.created_on.readable = db.recipe.created_on.writable = False
db.recipe.created_by.readable = db.recipe.created_by.writable = False
db.recipe.rating.readable = db.recipe.rating.writable = False

# table of recipe comments
db.define_table('post',
   Field('recipe_id', 'reference recipe'),
   Field('author'),
   Field('body', 'text'),
   Field('created_on', 'datetime', default=request.now),
)

db.post.recipe_id.requires = IS_IN_DB(db, db.recipe.id, '%(titles)s')
db.post.body.requires = IS_NOT_EMPTY()
db.post.author.readable = db.post.author.writable = False
db.post.recipe_id.readable = db.post.recipe_id.writable = False
db.post.created_on.readable = db.post.created_on.writable = False

#
# The following three tables make up the coordinates of the 3-tuples of
# an ingredient description.
#
db.define_table('ingredient',
   Field('name', unique=True),
   # list of recipes that reference this ingredient, use for 
   # search-by-ingredients
   Field('recipe_reference_list', 'list:reference recipe', default=None),
   Field('created_on', 'datetime', default=request.now),
   Field('created_by', 'reference auth_user', default=auth.user_id)
)

