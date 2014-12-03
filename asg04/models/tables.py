db.define_table('president',
    Field('name'),
    Field('counter', 'integer', default=0),
    Field('master_counter', 'integer', default=0))
