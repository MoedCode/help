#!/bin/bash

# API Base URL
BASE_URL="http://127.0.0.1:8000/api"

# User credentials
USERNAME="john_doee"
PASSWORD='Joh_M$25xo'

# Profile update details
BIO="ProEng back end django developer"
IMAGE_PATH="/mnt/c/Users/Active/Pictures/Camera Roll/FB_IMG_1684853676131.jpg"

# Cookies file
COOKIES="cookies.txt"

# Get CSRF Token
echo "Fetching CSRF token..."
curl -c "$COOKIES" -X GET "$BASE_URL/csrf"

# Extract CSRF Token
CSRF_TOKEN=$(grep csrftoken "$COOKIES" | awk '{print $7}')
echo "CSRF Token: $CSRF_TOKEN"

# Login request
echo "Logging in as $USERNAME..."
curl -b "$COOKIES" -c "$COOKIES" -X POST "$BASE_URL/login/" \
     -H "Content-Type: application/json" \
     -H "X-CSRFToken: $CSRF_TOKEN" \
     -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}"

# Update profile with image and bio
echo "Updating profile..."
curl -b "$COOKIES" -c "$COOKIES" -X PUT "$BASE_URL/profile_update/" \
     -H "X-CSRFToken: $CSRF_TOKEN" \
     -F "profile_image=@$IMAGE_PATH" \
     -F "bio=$BIO"

echo "Profile update completed!"
