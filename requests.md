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
    "country": "USA",
    "profile_image": "john_doee.jpg"
}
```

#### **Register User 2**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/register/
```
**Request Body:**
```json
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
    "country": "USA",
    "profile_image": "john_doee.jpg"
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
{
    "username": "john_doee",
    "password": "Joh_M$25xo"
}
```

#### **Login User 2**
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

### **4. Create a Group**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/groups/create/
```
**Request Body:**
```json
{
    "username": "john_doee",
    "password": "Joh_M$25xo",
    "group_name": "Tech Enthusiasts",
    "group_description": "A group for people interested in technology."
}
```

---

### **5. Add User to Group**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/groups/add-user/
```
**Request Body:**
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "add_username": "max_john_doee"
}
```

---

### **6. Remove User from Group**
Send a `POST` request to:
```http
http://127.0.0.1:8000/api/groups/remove-user/
```
**Request Body:**
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "remove_username": "max_john_doee"
}
```

---

### **7. Test the Search Endpoint for Classes**
Send a `GET` request to:
```http
http://127.0.0.1:8000/api/classes/search/?query=Tech
```
**Headers:**
```http
X-CSRFToken: <the obtained CSRF token>
Authorization: Token <your_auth_token>
```

This request should return all `Classes` that match the search query `"Tech"`. Let me know if you need modifications! 🚀