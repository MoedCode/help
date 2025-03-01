
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
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        username = request.data.get("username")
        # password = request.data.get("password")
        group_name = request.data.get("group_name")
        contact_name = request.data.get("contact_name")
        group_description = request.data.get("group_description")

        # Authenticate user
        # user = authenticate(username=username, password=password)
        user = request.user

        if user is None or isinstance(user, AnonymousUser):
            return Response({"error": "Invalid username or password"}, status=S401)

        # Check if user is logged in
        # if not request.user.is_authenticated:
        #     return Response({"error": "User must be logged in"}, status=S403)
        if Groups.objects.filter(name=group_name).exclude(id=group.id).exists():
            return Response({"error": f"The group name '{group_name}' already exists."}, status=S.HTTP_400_BAD_REQUEST)
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


class UpdateGroup(APIView):
    """Allows a group admin to update group details."""

    permission_classes = [IsAuthenticated]  # Only authenticated users can update

    def post(self, request):
        data = request.data
        group_id = data.get("group_id")
        group_name = data.get("group_name")
        update_data = data.get("update_data", {})

        if not group_id and not group_name:
            return Response({"error": "Either 'group_id' or 'group_name' is required."}, status=S.HTTP_400_BAD_REQUEST)

        # Retrieve group using group_id or group_name
        if group_id:
            group = get_object_or_404(Groups, id=group_id)
        else:
            group = get_object_or_404(Groups, name=group_name)

        # Ensure the user is the admin
        if request.user != group.admin_user:
            return Response({"error": "You are not authorized to update this group."}, status=S.HTTP_403_FORBIDDEN)

        # Validate update_data fields
        allowed_fields = {"name", "description"}
        invalid_fields = set(update_data.keys()) - allowed_fields
        if invalid_fields:
            return Response({"error": f"Invalid fields: {', '.join(invalid_fields)}. Allowed fields: {', '.join(allowed_fields)}."}, status=S.HTTP_400_BAD_REQUEST)

        # Check for uniqueness if updating 'name'
        new_name = update_data.get("name")
        if new_name and new_name != group.name:
            if Groups.objects.filter(name=new_name).exclude(id=group.id).exists():
                return Response({"error": f"The group name '{new_name}' already exists."}, status=S.HTTP_400_BAD_REQUEST)

        # Track updates
        updated = False
        unchanged_fields = []

        for field, value in update_data.items():
            if hasattr(group, field):
                if getattr(group, field) != value:
                    setattr(group, field, value)
                    updated = True
                else:
                    unchanged_fields.append(field)

        if updated:
            group.save()
            return Response({"message": "Group updated successfully."}, status=S.HTTP_200_OK)

        # Provide clear reasons for no update
        if not update_data:
            return Response({"error": "No update data provided."}, status=S.HTTP_400_BAD_REQUEST)

        if unchanged_fields:
            return Response({"error": f"No changes detected. Fields already have the same values: {', '.join(unchanged_fields)}."}, status=S.HTTP_400_BAD_REQUEST)

        return Response({"error": "No valid updates were made."}, status=S.HTTP_400_BAD_REQUEST)

class AddUserToGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_identifier = request.data.get("group_name") or request.data.get("group_id")
        admin_username = request.data.get("admin_username")
        username = request.data.get("username")
        contact_name = request.data.get("contact_name")

        # Validate input fields
        if not group_identifier or not admin_username or not username or not contact_name:
            return Response({"error": "Missing required fields"}, status=S.HTTP_400_BAD_REQUEST)

        # Check if admin user exists
        admin_user = Users.objects.filter(username=admin_username).first()
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Invalid or unauthenticated admin user"}, status=S.HTTP_401_UNAUTHORIZED)

        # Find the group by ID or name
        group = None
        if isinstance(group_identifier, int):
            group = Groups.objects.filter(id=group_identifier).first()
        else:
            group = Groups.objects.filter(name=group_identifier).first()

        if not group:
            return Response({"error": "Group not found"}, status=S.HTTP_404_NOT_FOUND)

        # Ensure only the group's admin can add users
        if group.admin_user != admin_user:
            return Response({"error": "Only the group admin can add users"}, status=S.HTTP_403_FORBIDDEN)

        # Check if the user to be added exists
        add_user = Users.objects.filter(username=username).first()
        if not add_user:
            return Response({"error": "User to be added not found"}, status=S.HTTP_404_NOT_FOUND)

        # **Check if the user is already a group member**
        if group.members.filter(id=add_user.id).exists():
            return Response({"error": "User is already in the group"}, status=S.HTTP_400_BAD_REQUEST)

        # **Check if contact_name is already in GroupContact for this group**
        if GroupContact.objects.filter(group=group, contact_name=contact_name).exists():
            return Response({"error": "Contact name already exists in the group"}, status=S.HTTP_400_BAD_REQUEST)

        # Add user to group
        group.members.add(add_user)

        # Create GroupContact entry
        group_contact = GroupContact.objects.create(user=add_user, group=group, contact_name=contact_name or add_user.username)
        group_contact.save()

        return Response({"message": f"{username} added to {group.name} successfully as {contact_name}"}, status=S.HTTP_200_OK)
class RemoveUserFromGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"\n\nrequest header\n\n")
        group_identifier = request.data.get("group_name") or request.data.get("group_id")
        admin_username = request.data.get("admin_username")
        username = request.data.get("username")
        contact_name = request.data.get("contact_name")
        # Validate input
        if not all([group_identifier, admin_username]) or not all(["username, contact_name"]):
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

        user =None;
        if not username:
            contact = GroupContact.objects.filter(contact_name=contact_name).first()
            user = contact.user
        else:
            user = Users.objects.filter(username=username).first()


        if not user:
            return Response({"error": "User to be removed not found"}, status=S404)

        # Check if the user is in the group
        if user not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status=S400)

        # Remove user from group
        group.members.remove(user)
        return Response({"message": f"{username} removed from {group.name} successfully"}, status=S200)

class GetUpdateGroupContacts(APIView):
    """Handles retrieving and updating group contacts."""
    def post(self, request):
        """
        Fetch group contacts. If `contact_name` is provided, return that contact.
        Otherwise, return all contacts in the group, excluding the admin.
        """
        group_id = request.data.get("group_id")
        contact_name = request.data.get("contact_name")  # Optional

        if not group_id:
            return Response({"error": "group_id is required"}, status=S.HTTP_400_BAD_REQUEST)

        group = get_object_or_404(Groups, id=group_id)
        admin_user = group.admin_user  # Get the admin of the group

        if contact_name:
            # Look for the contact in GroupContact
            contact = GroupContact.objects.filter(group=group, contact_name=contact_name).first()

            if not contact:
                # If contact_name doesn't exist, check if user exists in group
                user = Users.objects.filter(group_memberships__group=group, username=contact_name).first()
                if user:
                    # Return default data for a group member without a contact entry
                    return Response({
                        "contact_name": user.username,  # Default to username
                        "mobile_number": user.mobile_number,
                        "user_id": user.id
                    }, status=S.HTTP_200_OK)
                return Response({"error": "Contact not found"}, status=S.HTTP_404_NOT_FOUND)

            # Return found contact details
            return Response({
                "contact_name": contact.contact_name or contact.user.username,
                "mobile_number": contact.user.mobile_number if contact.user else None,
                "user_id": contact.user.id if contact.user else None
            }, status=S.HTTP_200_OK)

        # If no contact_name is provided, return all contacts in the group, excluding the admin
        contacts = GroupContact.objects.filter(group=group).select_related("user")

        contact_list = [{
            "contact_name": c.contact_name or c.user.username,
            "mobile_number": c.user.mobile_number if c.user else None,
            "user_id": c.user.id if c.user else None
        } for c in contacts if c.user != admin_user]  # Exclude admin from list

        return Response(contact_list, status=S.HTTP_200_OK)

    def put(self, request):
        """Update the contact name of a group member."""
        group_id = request.data.get("group_id")
        user_id = request.data.get("user_id")
        new_contact_name = request.data.get("contact_name")

        if not group_id or not user_id or not new_contact_name:
            return Response({"error": "group_id, user_id, and contact_name are required"}, status=S.HTTP_400_BAD_REQUEST)

        group = get_object_or_404(Groups, id=group_id)
        user = get_object_or_404(Users, id=user_id)

        # Ensure the user is a member of the group
        if user not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status=S.HTTP_403_FORBIDDEN)

        # Find or create a GroupContact instance
        contact, created = GroupContact.objects.get_or_create(user=user, group=group)
        contact.contact_name = new_contact_name
        contact.save()

        return Response({"message": "Contact updated successfully"}, status=S.HTTP_200_OK)