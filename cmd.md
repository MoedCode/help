error in  browser
```

AssertionError at /api/profile_update/
You passed a Serializer instance as data, but probably meant to pass serialized `.data` or `.error`. representation.
Request Method:	PUT
Request URL:	http://127.0.0.1:8000/api/profile_update/
Django Version:	4.2.10
Exception Type:	AssertionError
Exception Value:
You passed a Serializer instance as data, but probably meant to pass serialized `.data` or `.error`. representation.
Exception Location:	/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/response.py, line 38, in __init__
Raised during:	api.views.ProfileUpdate
Python Executable:	/usr/bin/python3
Python Version:	3.8.10
Python Path:
['/mnt/c/Users/Active/Desktop/Coding/Gradutaion/help/help_backend',
 '/mnt/c/Users/Active/Desktop/Coding/Gradutaion/help/help_backend',
 '/mnt/c/Users/Active/Desktop/Coding/Gradutaion',
 '/usr/lib/python38.zip',
 '/usr/lib/python3.8',
 '/usr/lib/python3.8/lib-dynload',
 '/home/mohamed/.local/lib/python3.8/site-packages',
 '/usr/local/lib/python3.8/dist-packages',
 '/usr/lib/python3/dist-packages']
Server time:	Thu, 20 Feb 2025 14:05:21 +0000
Traceback Switch to copy-and-paste view
/home/mohamed/.local/lib/python3.8/site-packages/django/core/handlers/exception.py, line 55, in inner
                response = get_response(request) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/django/core/handlers/base.py, line 197, in _get_response
                response = wrapped_callback(request, *callback_args, **callback_kwargs) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/django/views/decorators/csrf.py, line 56, in wrapper_view
        return view_func(*args, **kwargs) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/django/views/generic/base.py, line 104, in view
            return self.dispatch(request, *args, **kwargs) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py, line 509, in dispatch
            response = self.handle_exception(exc) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py, line 469, in handle_exception
            self.raise_uncaught_exception(exc) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py, line 480, in raise_uncaught_exception
        raise exc …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py, line 506, in dispatch
            response = handler(request, *args, **kwargs) …
Local vars
/mnt/c/Users/Active/Desktop/Coding/Gradutaion/help/help_backend/api/views.py, line 362, in put
        return Response(serializer, S200) …
Local vars
/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/response.py, line 38, in __init__
            raise AssertionError(msg) …
Local vars

```


request
```json

{
    "bio": "Software engineer and tech enthusiast.",
    "profileimg": "profile_pics/john_doe.jpg",
    "profession": "Software Engineer",
    "location": "New York, USA",
    "verified": true
}


```

endpoint class


```py
class ProfileUpdate(APIView):
    """ Pofile Update Endpoint Class"""
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    def put(self, request):
        is_valid , result = validate_profile_update(request.data)
        if not is_valid:
            return Response(result, S400)
        # if request.user.is_auth:
        #     return Response({"error": "Unauthorized access."}, status=S403)

        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            try:
                profile = Profile.objects.create(user=request.user)
            except Exception as e:
                return Response({"error":str(e)}, S500)


        for field, value in result.items():
            setattr(profile, field, value)
        profile.save()
        serializer = ProfileSerializer(profile).dat
        return Response(serializer, S200)


```
serlaizeing class

```py
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile

        fields = "__all__"
```