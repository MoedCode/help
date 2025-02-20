get csrf token
http://127.0.0.1:8000/api/csrf

 add in next request  in headers section in request
 key : X-CSRFToken
 alue: <the obtained token >

# user1
## register
```json
{
    "username": "john_doee",
    "email": "john@examplee.com",
    "first_name": "Jfohn",
    "last_name": "Doe",
    "mobile_number": "2234567890",
    "date_of_birth": "1980-05-10",
    "password":"Joh_M$25xo",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA",
    "profile_image": "john_doee.jpg"
}

```
## login
```json
{
    "username": "john_doee",
    "password":"Joh_M$25xo"
}

```

# user2 register
```json
{
    "username": "max_john_doee",
    "email": "max@examplee.com",
    "first_name": "max",
    "last_name": "Doe",
    "mobile_number": "2134567890",
    "date_of_birth": "2000-05-10",
    "password":"Joh_M$25xo",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA",
    "profile_image": "john_doee.jpg"
}
```

# user2 update

```json
{
    "username": "max_john_doee",
    "password": "Joh_M$25xo",
    "update_data": {
        "email": "max.new@example.com",
        "first_name": "Maxwell",
        "last_name": "Doe",
        "mobile_number": "2134567899",
        "date_of_birth": "2000-05-10",
        "street": "456 Elm St",
        "city": "Los Angeles",
        "country": "USA",
        "profile_image": "max_new.jpg",
        "password": "NewP@ssw0rd123"
    }
}



```
# login user2
```json
{
    "username": "max_john_doee",
    "password":"Joh_M$25xo"
}

```


# create group

```json

{
    "username": "john_doee",
    "password": "Joh_M$25xo",
    "group_name": "Tech Enthusiasts",
    "group_description": "A group for people interested in technology."
}


```

# add user to the group
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "add_username": "max_john_doee"
}
```
# add user to the group
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "remove_username": "max_john_doee"
}

```
