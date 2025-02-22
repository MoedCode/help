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

# Ensure the cookies file is clean before starting
rm -f "$COOKIES"

# Login request (without CSRF, since it's disabled in Django)
echo "Logging in as $USERNAME..."
LOGIN_RESPONSE=$(curl -s -b "$COOKIES" -c "$COOKIES" -X POST "$BASE_URL/login/" \
     -H "Content-Type: application/json" \
     -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

# Check if login was successful
if echo "$LOGIN_RESPONSE" | grep -q "error"; then
    echo "Login failed: $LOGIN_RESPONSE"
    exit 1
fi

echo "Login successful!"

# Extract session ID from cookies
SESSION_ID=$(grep sessionid "$COOKIES" | awk '{print $7}')
if [ -z "$SESSION_ID" ]; then
    echo "Failed to retrieve session ID. Exiting."
    exit 1
fi
echo "Session ID: $SESSION_ID"

# Update profile with image and bio
echo "Updating profile..."
UPDATE_RESPONSE=$(curl -s -b "$COOKIES" -c "$COOKIES" -X PUT "$BASE_URL/profile_update/" \
     -H "Content-Type: multipart/form-data" \
     -F "profile_image=@$IMAGE_PATH" \
     -F "bio=$BIO")

# Check if update was successful
if echo "$UPDATE_RESPONSE" | grep -q "error"; then
    echo "Profile update failed: $UPDATE_RESPONSE"
    exit 1
fi

echo "Profile update completed successfully!"
