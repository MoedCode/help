from .main_views import *


class SetLocations(APIView):
    """
    API endpoint for setting, updating, retrieving, and deleting a user's locations.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a new location for the authenticated user."""
        user = request.user
        data = request.data

        # Ensure required fields are present
        required_fields = {"city", "country", "latitude", "longitude"}
        if not required_fields.issubset(data.keys()):
            return Response({"error": f"Missing required fields: {required_fields - data.keys()}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate location data
        is_valid, result = validate_location(data)
        if not is_valid:
            return Response({"errors": result}, status=status.HTTP_400_BAD_REQUEST)

        # Save the location instance
        location = Locations.objects.create(user=user, **result)
        serializer = LocationsSerializer(location)

        return Response(
            {"message": "Location saved successfully!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        """Update an existing location for the authenticated user."""
        user = request.user
        data = request.data

        location_id = data.get("id")
        if not location_id:
            return Response({"error": "Location ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = Locations.objects.get(id=location_id, user=user)
        except Locations.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate updated location data
        is_valid, result = validate_location(data)
        if not is_valid:
            return Response({"errors": result}, status=status.HTTP_400_BAD_REQUEST)

        # Update location instance
        for key, value in result.items():
            setattr(location, key, value)
        location.save()

        serializer = LocationsSerializer(location)
        return Response(
            {"message": "Location updated successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request, id=None):
        """Delete a specific location by ID (from URL or request data)."""
        user = request.user
        location_id = id or request.data.get("id")

        if not location_id:
            return Response({"error": "Location ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = Locations.objects.get(id=location_id, user=user)
            location.delete()
            return Response({"message": "Location deleted successfully"}, status=status.HTTP_200_OK)
        except Locations.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None):
        """Retrieve all locations or a specific one by ID."""
        user = request.user
        location_id = id or request.query_params.get("id")

        if location_id:
            try:
                location = Locations.objects.get(id=location_id, user=user)
                serializer = LocationsSerializer(location)
                return Response({"location": serializer.data}, status=status.HTTP_200_OK)
            except Locations.DoesNotExist:
                return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

        # If no ID is provided, return all locations
        locations = Locations.objects.filter(user=user)
        serializer = LocationsSerializer(locations, many=True)
        return Response({"locations": serializer.data}, status=status.HTTP_200_OK)

class DeleteAllLocations(APIView):
    """API endpoint to delete all locations for an authenticated user."""
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        deleted_count, _ = Locations.objects.filter(user=user).delete()
        return Response({"message": f"Deleted {deleted_count} locations"}, status=status.HTTP_200_OK)

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

    def post(self, request):
        """Create a new subscription package (Only for superusers)."""
        admin_user = self.authenticate_admin(request)
        if not admin_user:
            return Response(
                {"error": "Invalid admin credentials or insufficient permissions"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubscriptionPackageSerializer(data=request.data)
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

        serializer = SubscriptionPackageSerializer(package, data=request.data, partial=True)
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





from rest_framework.response import Response
from rest_framework.views import APIView
import json

class EchoRequestView(APIView):
    """An endpoint that returns the full request details and saves them to a file."""

    def handle_request(self, request):
        """Handles any request type and logs all details."""

        # Extract request headers
        headers = {key: value for key, value in request.headers.items()}

        # Extract request body safely
        try:
            body = request.body.decode('utf-8').strip()
            json_body = json.loads(body) if body else {}
        except json.JSONDecodeError:
            json_body = {"error": "Invalid JSON"}

        # Build full request data
        request_data = {
            "method": request.method,
            "path": request.get_full_path(),
            "headers": headers,
            "query_params": request.query_params.dict(),  # Query string params
            "body": json_body,
            "user": str(request.user) if request.user.is_authenticated else "Anonymous",
            "user_agent": headers.get("User-Agent", "Unknown"),
        }

        # Save request details to a JSON file
        with open("test.json", 'w') as log_file:
            json.dump(request_data, log_file, indent=4)

        return Response(request_data)

    # Allow all HTTP methods
    def get(self, request): return self.handle_request(request)
    def post(self, request): return self.handle_request(request)
    def put(self, request): return self.handle_request(request)
    def patch(self, request): return self.handle_request(request)
    def delete(self, request): return self.handle_request(request)
