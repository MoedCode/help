
from api.views_main import *


class GroupMembersData(APIView):
    """Retrieve all members of a given group."""
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        """Return all members of the specified group."""
        try:
            group_id = request.data.get("group_id")  # ✅ Corrected data retrieval

            # ✅ Validate group existence
            group = Groups.objects.filter(id=group_id).first()
            if not group:
                return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

            all_objects = []
            groups_members = group.members.all()  # ✅ Corrected member retrieval

            for member in groups_members:
                member_data = {
                    "id":member.id,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "mobile_number": member.mobile_number,
                    "email": member.email,
                    "username": member.username,
                }
                if group.admin_user == member:
                    member_data["admin_user"] = True
                all_objects.append(member_data)

            return Response(all_objects, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserGroups(APIView):
    """Retrieve all groups the authenticated user belongs to."""
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        """Return all groups the logged-in user is a member of."""
        user = request.user
        groups = Groups.objects.filter(admin_user=user)  # Get groups where user is a member
        serializer = GroupsSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CreateGroup(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        group_name = request.data.get("group_name")
        contact_name = request.data.get("contact_name")
        group_description = request.data.get("group_description")

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None or isinstance(user, AnonymousUser):
            return Response({"error": "Invalid username or password"}, status=S401)

        # Check if user is logged in
        # if not request.user.is_authenticated:
        #     return Response({"error": "User must be logged in"}, status=S403)

        # Create new group
        group = Groups.objects.create(
            name=group_name,
            description=group_description,
            admin_user=user  # Assuming the Group model has an 'admin' field
        )
        group_contact =GroupContact.objects.create(user=user, group=group, contact_name = contact_name or user.username)
        group_contact.save()
        group.members.add(user)  # Add user as a member
        return Response({"message": "Group created successfully", "group_id": group.id}, status=S201)


class AddUserToGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_identifier = request.data.get("group_name") or request.data.get("group_id")
        admin_username = request.data.get("admin_username")
        add_username = request.data.get("add_username")
        contact_name = request.data.get("contact_name")

        # Validate input
        if not all([group_identifier, admin_username, add_username]):
            return Response({"error": "Missing required fields"}, status=S400)

        # Check if admin user exists
        admin_user = Users.objects.filter(username=admin_username).first()
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Invalid or unauthenticated admin user"}, status=S401)

        # Find the group by name or ID
        group = None
        if isinstance(group_identifier, int):  # If group_id is given
            group = Groups.objects.filter(id=group_identifier).first()
        else:  # If group_name is given
            group = Groups.objects.filter(name=group_identifier).first()

        if not group:
            return Response({"error": "Group not found"}, status=S404)

        # Check if admin user is the group's admin
        if group.admin_user != admin_user:
            return Response({"error": "Only the group admin can add users"}, status=S403)

        # Check if the user to be added exists
        add_user = Users.objects.filter(username=add_username).first()
        if not add_user:
            return Response({"error": "User to be added not found"}, status=S404)

        # Add user to group
        group.members.add(add_user)
        group_contact =GroupContact.objects.create(user=add_user, group=group, contact_name = contact_name or user.username)
        group_contact.save()

        return Response({"message": f"{add_username} added to {group.name} successfully"}, status=S200)
class RemoveUserFromGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"\n\nrequest header\n\n")
        group_identifier = request.data.get("group_name") or request.data.get("group_id")
        admin_username = request.data.get("admin_username")
        remove_username = request.data.get("remove_username")

        # Validate input
        if not all([group_identifier, admin_username, remove_username]):
            return Response({"error": "Missing required fields"}, status=S400)

        # Check if admin user exists and is authenticated
        admin_user = Users.objects.filter(username=admin_username).first()
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Invalid or unauthenticated admin user"}, status=S401)

        # Find the group by name or ID
        group = None
        if isinstance(group_identifier, int):  # If group_id is given
            group = Groups.objects.filter(id=group_identifier).first()
        else:  # If group_name is given
            group = Groups.objects.filter(name=group_identifier).first()

        if not group:
            return Response({"error": "Group not found"}, status=S404)

        # Check if admin user is the group's admin
        if group.admin_user != admin_user:
            return Response({"error": "Only the group admin can remove users"}, status=S403)

        # Check if the user to be removed exists
        remove_user = Users.objects.filter(username=remove_username).first()
        if not remove_user:
            return Response({"error": "User to be removed not found"}, status=S404)

        # Check if the user is in the group
        if remove_user not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status=S400)

        # Remove user from group
        group.members.remove(remove_user)
        return Response({"message": f"{remove_username} removed from {group.name} successfully"}, status=S200)
