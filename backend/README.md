## Running
```
flask run
```

### Commands
```
curl -H "Content-Type: application/json" -d '{"email":"test@test.com","pass":"password"}' http://127.0.0.1:5000/login

{'iat': 1577472722, 'nbf': 1577472722, 'jti': '3015714c-3877-4499-a735-df064ae368e6', 'exp': 1577473622, 'identity': 'test@test.com', 'fresh': False, 'type': 'access', 'user_claims': {'role': 'User'}}

curl -H 'Accept: application/json' -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzc0NzA0MDksIm5iZiI6MTU3NzQ3MDQwOSwianRpIjoiNTU2MmZlOTktNzUwZC00ZjE3LTk4NjYtNDIwNzI3YWQzY2FkIiwiZXhwIjoxNTc3NDcxMzA5LCJpZGVudGl0eSI6InRlc3RAdGVzdC5jb20iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJyb2xlIjoiVXNlciJ9fQ.eSBF9VV84KRy7BXtmyccaDC-ftZaJ10yfUHYuGmH1jc" http://0:5000/graphql
```

## Query
http://127.0.0.1:5000/graphql?query=%7B%0A%20%20allUsers%7B%0A%20%20%20%20edges%7B%0A%20%20%20%20%20%20node%7B%0A%20%20%20%20%20%20%20%20uuid%0A%20%20%20%20%20%20%20%20email%0A%20%20%20%20%20%20%20%20password%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D


## Mutation
http://127.0.0.1:5000/graphql?query=mutation%20%7B%0A%20%20createUser(email%3A%20%22test%40test.com%22%2C%20name%3A%20%22David%22%2C%20password%3A%20%22password%22)%20%7B%0A%20%20%09user%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20email%0A%20%20%20%20%20%20uuid%0A%20%20%20%20%20%20id%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D&operationName=undefined