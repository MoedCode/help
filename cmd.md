in postman in  cookies section after i logged in

```
No cookies received from the server
All your cookies and their associated domains will appear here.
```
request
```json

{
    "username": "john_doee",
    "password":"Joh_M$25xo"
}


```
endpoint
```py
class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Check if both fields are provided
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=S400)

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # Start session
            serializer = UsersSerializer(user, context={"request": request})
            return Response({"message": "Login successful", "user": serializer.data}, status=S200)
        else:
            return Response({"error": "Invalid credentials"}, status=S401)



```