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
    """ display top rated, viewed, and recent posts """
    top_viewed = db(db.recipe).select(db.recipe.ALL, 
                   orderby=~db.recipe.hits, limitby=(0,6))
    recent_posts = db(db.recipe).select(db.recipe.ALL, 
                   orderby=~db.recipe.created_on, limitby=(0,6))
    return dict(top_viewed=top_viewed, recent_posts=recent_posts)

def search_results():
    """ diplays search results """
    search_url = URL('search')
    result = request.args
    recipes = []
    for recipe_id in result:
        recipe = db(db.recipe.id==recipe_id).select().first()
        recipes.append(recipe)
    return dict(recipes=recipes, search_url=search_url)


def search():
    """ search for a recipe by ingredient list """
    form = SQLFORM.factory(
               Field('ingredients', 'list:string', requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        refs_list = []
        for name in form.vars.ingredients:
            ingredient = db(db.ingredient.name==name).select().first()
            if ingredient is None:
                refs_list.append([])
            else:
                refs_list.append(ingredient.recipe_reference_list)
        result = list(set(refs_list[0]).intersection(*refs_list))
        redirect (URL('search_results', args=result))
    if form.errors:
        response.flash = 'form contains errors'
    return dict(form=form)


def view():
    """ displays a recipe """
    recipe = db(db.recipe.id==request.args(0, cast=int)).select().first()
    if recipe is not None:
        # get rating info
        form = SQLFORM(db.post, separator='', labels={'body':''})
        form.vars.recipe_id = recipe.id
        if auth.user is not None:
            form.vars.author = auth.user.first_name
        if form.process().accepted:
            response.flash = 'your comment was posted'
        comments = db(db.post.recipe_id==recipe.id).select()
        recipe.hits += 1
        recipe.update_record()
        return dict(recipe=recipe, comments=comments, 
                    form=form)
    else:
        raise HTTP(404)


def update_ingredient_references(form):
    """ creates/adds references from each ingredient to this recipe """
    ilist = form.vars.ingredient_list
    if len(ilist)==1:
        row = db(db.ingredient.name==ilist).select().first()
        if row is not None:
            row.recipe_reference_list.append(form.vars.id) 
            row.update_record()
        else:
            db.ingredient.insert(
                name=ingredient,
                recipe_reference_list=[form.vars.id],
            )
    else:
        for ingredient in form.vars.ingredient_list:
            row = db(db.ingredient.name==ingredient).select().first()
            if row is not None:
                row.recipe_reference_list.append(form.vars.id) 
                row.update_record()
            else:
                db.ingredient.insert(
                    name=ingredient,
                    recipe_reference_list=[form.vars.id],
                )


@auth.requires_login()
def create():
    """ create a new recipe  """
    form = SQLFORM(db.recipe, labels={'ingredient_list':'Main Ingredients'},
                              formstyle="table2cols")
    if form.process().accepted:
       update_ingredient_references(form)
       redirect(URL('view', args=[form.vars.id]))
    elif form.errors:
       response.flash = 'recipe contains errors'
    return dict(form=form)


@auth.requires_login()
def my_recipes():
    """ displays all user uploaded recipes """
    user_recipes = db(db.recipe.created_by==auth.user.id)
    recipes = user_recipes.select(db.recipe.ALL, orderby=db.recipe.title)
    return dict(recipes=recipes)


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

response.menu = [
    ['Home',      False, URL('index')],
    ['Search',    False, URL('search')],
    ['Post',      False, URL('create')],
    ['MyRecipes', False, URL('my_recipes')]
] 
