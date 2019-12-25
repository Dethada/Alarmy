## Running
```
flask run
```

## Query
http://127.0.0.1:5000/graphql?query=%7B%0A%20%20allUsers%7B%0A%20%20%20%20edges%7B%0A%20%20%20%20%20%20node%7B%0A%20%20%20%20%20%20%20%20uuid%0A%20%20%20%20%20%20%20%20email%0A%20%20%20%20%20%20%20%20password%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D


## Mutation
http://127.0.0.1:5000/graphql?query=mutation%20%7B%0A%20%20createUser(email%3A%20%22test%40test.com%22%2C%20name%3A%20%22David%22%2C%20password%3A%20%22password%22)%20%7B%0A%20%20%09user%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20email%0A%20%20%20%20%20%20uuid%0A%20%20%20%20%20%20id%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D&operationName=undefined