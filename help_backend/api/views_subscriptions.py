from api.views_main import *
class SubscriptionPackageView(APIView):
    """
    API endpoint for creating, updating, and deleting subscription packages.
    Requires an application admin (superuser) to be logged in
    and to provide a valid admin username & password.
    """
    permission_classes = [IsAuthenticated]

    def authenticate_admin(self, request):
        """Helper function to authenticate an admin user."""
        admin_username = request.data.get("admin_username")
        admin_password = request.data.get("admin_password")
        admin_user = authenticate(username=admin_username, password=admin_password)

        if not admin_user or not admin_user.is_superuser:
            return None

        return admin_user
    def get(self, request):
            """Retrieve all available subscription packages"""
            packages = SubscriptionPackage.objects.all()
            serializer = SubscriptionPackagesSerializer(packages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new subscription package (Only for superusers)."""
        admin_user = self.authenticate_admin(request)
        if not admin_user:
            return Response(
                {"error": "Invalid admin credentials or insufficient permissions"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubscriptionPackagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=admin_user)
            return Response(
                {"message": "Subscription package created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update an existing subscription package (Only for superusers)."""
        admin_user = self.authenticate_admin(request)
        if not admin_user:
            return Response(
                {"error": "Invalid admin credentials or insufficient permissions"},
                status=status.HTTP_403_FORBIDDEN
            )

        package_id = request.data.get("id")
        if not package_id:
            return Response({"error": "Subscription package ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            package = SubscriptionPackage.objects.get(id=package_id)
        except SubscriptionPackage.DoesNotExist:
            return Response({"error": "Subscription package not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionPackagesSerializer(package, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Subscription package updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete a subscription package (Only for superusers)."""
        admin_user = self.authenticate_admin(request)
        if not admin_user:
            return Response(
                {"error": "Invalid admin credentials or insufficient permissions"},
                status=status.HTTP_403_FORBIDDEN
            )

        package_id = request.data.get("id")
        if not package_id:
            return Response({"error": "Subscription package ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            package = SubscriptionPackage.objects.get(id=package_id)
            package.delete()
            return Response({"message": "Subscription package deleted successfully"}, status=status.HTTP_200_OK)
        except SubscriptionPackage.DoesNotExist:
            return Response({"error": "Subscription package not found"}, status=status.HTTP_404_NOT_FOUND)



