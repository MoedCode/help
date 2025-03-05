# To **install and enable SSH** on your Ubuntu server, follow these steps:
```
---

### **1️⃣ Install OpenSSH Server**
Run the following command:

```bash
sudo apt update && sudo apt install -y openssh-server
```

---

### **2️⃣ Start & Enable SSH Service**
After installation, start the SSH service and enable it to start on boot:

```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```

To check if SSH is running:

```bash
sudo systemctl status ssh
```

If SSH is running correctly, you should see:

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) ...
```

---

### **3️⃣ Allow SSH in Firewall (if enabled)**
If your firewall (`ufw`) is enabled, allow SSH connections:

```bash
sudo ufw allow ssh
```

To check firewall status:

```bash
sudo ufw status
```

---

### **4️⃣ Find Server IP Address**
Run:

```bash
hostname -I
```

Example output:

```
192.168.0.107 10.0.0.5
```

---

### **5️⃣ Connect to Server via SSH**
From another computer, use this command:

```bash
ssh username@server-ip
```

Example:

```bash
ssh help@192.168.0.107
```

If you're connecting for the first time, type **yes** to accept the key fingerprint.

---

Now your Ubuntu server should be accessible via SSH! 🚀 Let me know if you need further help.

```
# python3 update
```sh

#!/bin/bash

echo "Updating System Packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing required dependencies..."
sudo apt install -y software-properties-common

echo "Adding Deadsnakes PPA (Latest Python Versions)..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

echo "Installing the Latest Python3 Version..."
sudo apt install -y python3 python3-dev python3-venv python3-pip

echo "Upgrading pip3..."
python3 -m pip install --upgrade pip

echo "Setting Python3 as Default..."
update-alternatives --install /usr/bin/python python /usr/bin/python3 1

echo "Cleaning Unused Packages..."
sudo apt autoremove -y

echo "✅ Python and pip updated successfully!"
python3 --version
pip3 --version
````
# sudo vim /etc/nginx/sites-available/wecareroot 0
```nginx
server {
    listen 5595;
    server_name wecareroot.ddns.net; # Your DDNS Hostname

    location / {
        proxy_pass http://127.0.0.1:8000/; # Django Backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}



```
server {
    listen 5595;
    server_name wecareroot.ddns.net;

    location /.well-known/acme-challenge/ {
        allow all;
        root /var/www/html;
    }

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

