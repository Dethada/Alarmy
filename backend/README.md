## Flask Migrate
```
flask db init    # initalize config
flask db migrate # generate migration
flask db upgrade # apply migration
```

## Running
```
pipenv run ./app.py
```

### Development Commands
```
curl -H "Content-Type: application/json" -d '{"email":"admin@admin.com","pass":"password"}' http://127.0.0.1:5000/token/auth

{'iat': 1577472722, 'nbf': 1577472722, 'jti': '3015714c-3877-4499-a735-df064ae368e6', 'exp': 1577473622, 'identity': 'test@test.com', 'fresh': False, 'type': 'access', 'user_claims': {'role': 'User'}}

curl -H 'Accept: application/json' -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzc0NzA0MDksIm5iZiI6MTU3NzQ3MDQwOSwianRpIjoiNTU2MmZlOTktNzUwZC00ZjE3LTk4NjYtNDIwNzI3YWQzY2FkIiwiZXhwIjoxNTc3NDcxMzA5LCJpZGVudGl0eSI6InRlc3RAdGVzdC5jb20iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJyb2xlIjoiVXNlciJ9fQ.eSBF9VV84KRy7BXtmyccaDC-ftZaJ10yfUHYuGmH1jc" http://0:5000/graphql
```

## Dependencies
```
flask = "*"
flask-graphql = "*"
flask-migrate = "*"
flask-sqlalchemy = "*"
graphene = "*"
graphene-sqlalchemy = "*"
sqlalchemy-utils = "*"
argon2-cffi = "*"
flask-jwt-extended = "*"
flask-cors = "*"
psycopg2 = "*"
gevent-websocket = "*" # choose 1 shld work
gunicorn = "*" # choose 1 shld work
eventlet = "*" # choose 1 shld work
flask-socketio = "*"
pandas = "*"
python-dotenv = "*"
sendgrid = "*"
numpy = "*" # installed by pandas?
google-cloud-iot = "*"
```
