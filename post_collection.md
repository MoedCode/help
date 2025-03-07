### ✅ 1. Get CSRF Token
Send a `GET` request to:
```http
http://wecareroot.ddns.net:5595/api/csrf
```
Save the response token and include it in the `X-CSRFToken` header for the next requests.

---

### ✅ 2. Register Users
#### **Register User 1**
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/register/
```
**Request Body:**
```json
{
    "username": "john_doee",
    "email": "john@examplee.com",
    "first_name": "John",
    "last_name": "Doe",
    "mobile_number": "2234567890",
    "date_of_birth": "1980-05-10",
    "password": "Joh_M$25xo",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA"
}
```
**Response:**
```json
{
    "username": "john_doee",
    "email": "john@examplee.com",
    "first_name": "John",
    "last_name": "Doe",
    "id": "288a86c3-5368-4f34-8df0-b9f6201d1cd2"
}
```

---

### ✅ 3. Update Users
Send a `PUT` request to:
```http
http://wecareroot.ddns.net:5595/api/user/update/
```
**Request Body:**
```json
{
    "username": "max_john_doee",
    "password": "Joh_M$25xo",
    "update_data": {
        "email": "max.new@example.com",
        "first_name": "MaxVerywell",
        "last_name": "Doe",
        "mobile_number": "2134567899",
        "street": "456 Elm St",
        "city": "Los Angeles",
        "country": "USA"
    }
}
```

---

### ✅ 4. Activate Users
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/activate/
```
**Request Body:**
```json
{
    "username": "max_john_doee",
    "code": "698693"
}
```
**Response:**
```json
{
    "message": "Account activated successfully"
}
```

---

### ✅ 5. Login Users
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/login/
```
**Request Body:**
```json
{
    "username": "john_doee",
    "password": "Joh_M$25xo"
}
```
**Response:**
```json
{
    "message": "Login successful",
    "user": {
        "username": "john_doee"
    }
}
```

---

### ✅ 6. Create Group
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/groups/create/
```
**Request Body:**
```json
{
    "username": "john_doee",
    "group_name": "Tech Enthusiasts",
    "contact_name": "john",
    "group_description": "A group for people interested in technology."
}
```
**Response:**
```json
{
    "message": "Group created successfully",
    "group_id": "a0f83d51-6588-4192-8567-a75205c44a9b"
}
```

---

### ✅ 7. Add User to Group
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/groups/add-user/
```
**Request Body:**
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "contact_name": "myFuckenSon",
    "username": "max_john_doee"
}
```
**Response:**
```json
{
    "message": "max_john_doee added to Tech Enthusiasts successfully as myFuckenSon"
}
```

---

### ✅ 8. Remove User from Group
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/groups/remove-user/
```
**Request Body:**
```json
{
    "group_name": "Tech Enthusiasts",
    "admin_username": "john_doee",
    "contact_name": "myFuckenSon",
    "username": "max_john_doee"
}
```
**Response:**
```json
{
    "message": "User removed successfully"
}
```

---

### ✅ 9. Set Profile Information
**Requires Login**
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/profile/
```
**Request Body:**
```json
{
    "bio": "Any bio",
    "profession": "Any Profession",
    "location": "Any Location"
}
```
**Response:**
```json
{
    "message": "Profile updated successfully"
}
```

---

### ✅ 10. Set User Location
Send a `POST` request to:
```http
http://wecareroot.ddns.net:5595/api/location/
```
**Request Body:**
```json
{
    "city": "New York",
    "country": "United States",
    "address": "Comp y, Strate x..dep number 12",
    "latitude": 40.7128,
    "longitude": -74.0060
}
```
**Response:**
```json
{
    "message": "Location updated successfully"
}
```

