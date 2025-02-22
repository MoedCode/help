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

# Step 1: Get CSRF Token
echo "Fetching CSRF token..."
curl -c "$COOKIES" -X GET "$BASE_URL/csrf"

# Extract CSRF Token from cookies.txt
CSRF_TOKEN=$(grep csrftoken "$COOKIES" | awk '{print $7}')
echo "CSRF Token: $CSRF_TOKEN"

# Step 2: Log in to get session ID
echo "Logging in as $USERNAME..."
LOGIN_RESPONSE=$(curl -s -b "$COOKIES" -c "$COOKIES" -X POST "$BASE_URL/login/" \
     -H "Content-Type: application/json" \
     -H "X-CSRFToken: $CSRF_TOKEN" \
     -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

# Check if login was successful
if echo "$LOGIN_RESPONSE" | grep -q "error"; then
    echo "Login failed: $LOGIN_RESPONSE"
    exit 1
fi
echo "Login successful!"

# Step 3: Extract session ID (optional, already stored in cookies.txt)
SESSION_ID=$(grep sessionid "$COOKIES" | awk '{print $7}')
echo "Session ID: $SESSION_ID"

# Step 4: Update profile with image and bio using session authentication
echo "Updating profile..."
UPDATE_RESPONSE=$(curl -s -b "$COOKIES" -X PUT "$BASE_URL/profile_update/" \
     -H "X-CSRFToken: $CSRF_TOKEN" \
     -H "Content-Type: multipart/form-data" \
     -F "profile_image=@$IMAGE_PATH" \
     -F "bio=$BIO")

# Check if profile update was successful
if echo "$UPDATE_RESPONSE" | grep -q "error"; then
    echo "Profile update failed: $UPDATE_RESPONSE"
    exit 1
fi

echo "Profile update completed successfully!"
