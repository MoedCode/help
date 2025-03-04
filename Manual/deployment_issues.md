[Step by Step WhatsApp Business API + Django Application ..video](https://youtu.be/6XZZKk1UxUQ?si=yjb-Xsq8FO63O5eT)


### 📌 All Problems & Solutions We Faced Until Your Django Rest Framework Application Worked
---

### 🛑 Problem 1: **Nginx Doesn't Serve Requests**
**Description:**
You installed Nginx, but your application didn't work on the hostname `wecareroot.ddns.net:5595`.

---

**Reason:**
✅ Nginx was running, but there was **no correct symbolic link** between:
```bash
/etc/nginx/sites-available/wecareroot
```
and
```bash
/etc/nginx/sites-enabled/
```
---

### 🔥 Solution:
1. First, delete the corrupted symbolic link:
```bash
sudo rm /etc/nginx/sites-enabled/wecareroot
```
2. Create a new symbolic link:
```bash
sudo ln -s /etc/nginx/sites-available/wecareroot /etc/nginx/sites-enabled/
```
3. Test Nginx configuration:
```bash
sudo nginx -t
```
✅ Output should be:
```bash
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
4. Restart Nginx:
```bash
sudo systemctl restart nginx
```
---

---

### 🛑 Problem 2: **Firewall Blocking Port 5595**
**Description:**
You allowed the port **5595** in the Nginx configuration, but the request didn't reach the server.

---

**Reason:**
The Ubuntu **UFW firewall** was blocking port 5595.

---

### 🔥 Solution:
1. Allow the port using UFW:
```bash
sudo ufw allow 5595/tcp
sudo ufw reload
```
---

---

### 🛑 Problem 3: **Invalid HTTP_HOST in Django (DisallowedHost Error)**
**Description:**
When you visited:
```bash
http://wecareroot.ddns.net/api/register/
```
You got this error:
```
Invalid HTTP_HOST header: 'wecareroot.ddns.net'. You may need to add 'wecareroot.ddns.net' to ALLOWED_HOSTS.
```
---

**Reason:**
Django by default blocks unknown domains unless you add them to **ALLOWED_HOSTS**.

---

### 🔥 Solution:
1. Open your `settings.py` file:
```bash
sudo vim /home/help/Downloads/help/help_backend/help/settings.py
```
2. Add your hostname to **ALLOWED_HOSTS** like this:
```python
ALLOWED_HOSTS = ['wecareroot.ddns.net', '127.0.0.1']
```
3. Restart Gunicorn or Django backend:
```bash
sudo systemctl restart gunicorn
```
---

---

### 🛑 Problem 4: **Port 8000 Not Listening Globally**
**Description:**
The backend was running on:
```bash
127.0.0.1:8000
```
---

**Reason:**
When Gunicorn or Django runs on **127.0.0.1**, Nginx can't access it from outside.

---

### 🔥 Solution:
Run your backend with this command:
```bash
python manage.py runserver 0.0.0.0:8000
```
---

---

### 🛑 Problem 5: **netstat Command Not Found**
**Description:**
When you tried to check which ports are listening:
```bash
sudo netstat -tuln
```
You got:
```bash
Command 'netstat' not found
```
---

### 🔥 Solution:
Install **net-tools** package:
```bash
sudo apt install net-tools -y
```
---

---

### 🔥 Final Steps to Start Everything:
1. Restart Nginx:
```bash
sudo systemctl restart nginx
```
2. Restart the backend:
```bash
sudo systemctl restart gunicorn
```
3. Check if Nginx is running:
```bash
sudo systemctl status nginx
```
---

---

### ✅ What Should Work Now?
| Service               | Status        |
|---------------------|-------------|
| Nginx              | ✅ Running |
| Django Backend     | ✅ Running |
| Firewall           | ✅ Open on Port 5595 |
| Symbolic Link      | ✅ Created |
| Hostname           | ✅ Allowed in Django |
---

---

### 🎯 Final Test:
Visit this link:
👉 http://wecareroot.ddns.net:5595/api/register/

---

---

### If It Works Say:
### **"El7amdoLellah Ro7t YA 7AGGGGG 🔥😂"**

---

If you still face any issues, I'll generate an automatic configuration file + deployment bash script 🚀💪.