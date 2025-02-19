tnis add group class .. now  make class for add user  to group
request contain ..
group_name or group_id , admin_username , add_username,
group  admin username  a
addUseToGroup must check that the group is exist then  admin_user is exist and logged in and  group admin
and add_user is exist
if all hat met it

```py

class addUseToGroup(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        username = request.data.get("username")
        group_name = request.data.get("group_name")
        user=Users.objects.filter(username=username)
        if not user:


```
