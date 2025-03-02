To test the **search endpoint** for the `Classes` API, follow these steps:

### **1. Get CSRF Token**
Send a `GET` request to:
```http
http://127.0.0.1:8000/api/csrf
```
Save the response token and include it in the `X-CSRFToken` header for the next requests.

---

### **2. Register Users**
#### **Register User 1**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/register/
```
**Request Body:**
```json
{
    "username": "john_doee",
    "email": "john@examplee.com",
    "first_name": "Jfohn",
    "last_name": "Doe",
    "mobile_number": "2234567890",
    "date_of_birth": "1980-05-10",
    "password": "Joh_M$25xo",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA"

}
// user 2

{
    "username": "max_john_doee",
    "email": "max@examplee.com",
    "first_name": "max",
    "last_name": "Doe",
    "mobile_number": "2134567890",
    "date_of_birth": "2000-05-10",
    "password": "Joh_M$25xo",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA"

}
// user3
{
    "username": "userX",
    "email": "userx@gmail.com",
    "first_name": "user",
    "last_name": "x",
    "mobile_number": "2734567690",
    "date_of_birth": "2000-05-10",
    "password": "Joh_M$25xo",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA"

}

```


**Response
```json
{
    "username": "userX",
    "email": "userx@gmail.com",
    "first_name": "user",
    "last_name": "x",
    "id": "288a86c3-5368-4f34-8df0-b9f6201d1cd2"
}

```
---

### **3. Login Users**
#### **Login User 1**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/login/
```
**Request Body:**
```json
// user2
{
    "username": "john_doee",
    "password": "Joh_M$25xo"
}
// user3
{
    "username": "userX",
    "password": "Joh_M$25xo"

}
```
**response

```json
{
    "message": "Login successful",
    "user": {
        "username": "userX"
    }
}
```
#### Login User 2
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/login/
```
**Request Body:**
```json
{
    "username": "max_john_doee",
    "password": "Joh_M$25xo"
}
```

---

### 4. Create a Group
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/groups/create/
```
**Request Body:**
*Group1*
```json
{
    "username": "john_doee",
    "group_name": "Tech Enthusiasts",
    "contact_name":"john",
    "group_description": "A group for people interested in technology."
}

{
    "username": "john_doee",
    "group_name": "__Tech_Enthusiasts__",
    "contact_name":"john",
    "group_description": "A group for people interested in technology."
}
```
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept
```response
{
    "message": "Group created successfully",
    "group_id": "a0f83d51-6588-4192-8567-a75205c44a9b"
}
```


```
## 5. update group
```url
    http://127.0.0.1:8000/api/update_group/
```
```json
{
    "group_id": "a598cc9f1e7d4ed1a57eea6d0967565",
    "update_data": {
        "name": "New Group Name",
        "description": "Updated description of the group."
    }
}



//OR

{
    "group_name": "Tech Enthusiasts",
    "update_data": {
        "name": "Tech Enthusiasts",
        "description": "Updated description of the group."
    }
}



```

---

### 5. Add User to Group
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/groups/add-user/
```
**Request Body:**
```json
// max_john_doee  to Tech Enthusiasts

{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "contact_name":"myFuckenSon",
    "username": "max_john_doee"
}
// userX to Tech Enthusiasts
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "contact_name":"myOtherAssHolSon",
    "username": "userX"
}

 // add user to group2

{
    "group_name": "__Tech_Enthusiasts__",
    "admin_username": "john_doee",
    "contact_name":"myFuckenSon",
    "username": "max_john_doee"
}
//add  user  3
{
    "group_name": "__Tech_Enthusiasts__",
    "admin_username": "john_doee",
    "contact_name":"myOtherAssHolSon",
    "username": "max_john_doee"
}
```
**response**
```json
{
    "message": "userX added to Tech Enthusiasts successfully as myOtherAssHolSon"
}
```

---

### **6. Remove User from Group**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/groups/remove-user/
```
**require login with group admin user**

**Request Body:**
need just to provide on of conatact_name or username and
both will nnot result to error
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "contact_name":"myFuckenSon",
    "username": "max_john_doee"
}
```

# update profile
**requires login**
 ## upload image file
```json

{
    "bio":"any bio ",
    "profession":"any Profession",
    "location":"any Location"
}


```
## group contacts
```json
{
    "group_id": "20055dc886384c1ab676118ee1357209"
}
```
**Response:**
```json
[
    {
        "contact_name": "john_doee",
        "mobile_number": "+1234567890",
        "user_id": 5
    },
    {
        "contact_name": "AliceSmith",
        "mobile_number": "+9876543210",
        "user_id": 12
    }
]
```

---

#### **🔹 Fetch Specific Contact**
**Request:**
```http
POST /api/group_contacts/
Content-Type: application/json
```
**Payload:**
```json
{
    "group_id": "923375cdf9424016845d0630b5912bb8",
    "contact_name": "john_doee"
}
```
**Response:**
```json
{
    "contact_name": "john_doee",
    "mobile_number": "2234567890",
    "user_id": "43441919-75ee-40ad-a0c7-ba2ff2452b44"
}
```

---

#### **🔹 Update a Contact Name**
**Request:**
```http
PUT /api/group_contacts/
Content-Type: application/json
```
**Payload:**
```json
{
    "group_id": "a598cc9f1e7d4ed1a57eea6d0967565",
    "user_id": 5,
    "contact_name": "John The Great"
}
```
**Response:**
```json
{
    "message": "Contact updated successfully"
}
```

---


# set a location
**requires login from user account**
```json
{
    "city": "New York",
    "country": "United States",
    "address":"comp y ,  strate x..dep number 12",
    "latitude": 40.7128,
    "longitude": -74.0060
}
{
"dist_mail":"sirmohamedh@gmail.com",
"dist_mail_body":"email body 4 test ",
"dist_mail_sub":"email subject 4 test ",
}



```
---

<!-- ### **7. Test the Search Endpoint for Classes**
Send a `GET` request to:
```http
http://127.0.0.1:8000/api/classes/search/?query=Tech
```
**Headers:**
```http
X-CSRFToken: <the obtained CSRF token>
Authorization: Token <your_auth_token>
```

This request should return all `Classes` that match the search query `"Tech"`. Let me know if you need modifications! 🚀 -->