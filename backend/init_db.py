#!/usr/bin/env python3
import uuid
from argon2 import PasswordHasher
from sqlalchemy import create_engine

db_uri = "sqlite:///data.sqlite"
engine = create_engine(db_uri)
ph = PasswordHasher()

# insert a raw
engine.execute('INSERT INTO "users" '
               '(uuid, email, name, role, password) '
               'VALUES ("{}", "admin@admin.com","Default Admin", "Admin", "{}")'.format(str(uuid.uuid4()), ph.hash('password')))

# select *
result = engine.execute('SELECT * FROM '
                        '"users"')
for _r in result:
   print(_r)

# result = engine.execute('SELECT * FROM "EX1"')
# print(result.fetchall())