from api.views_main import *

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
class RecentLcation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        try:
            recent_location = Locations.recent(user_id=user_id)
            serializer = LocationsSerializer(recent_location).data
            return Response(serializer, S200)
        except Exception as e:
            return Response({"error":str(e)}, S500)

class DeleteAllLocations(APIView):
    """API endpoint to delete all locations for an authenticated user."""
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        deleted_count, _ = Locations.objects.filter(user=user).delete()
        return Response({"message": f"Deleted {deleted_count} locations"}, status=status.HTTP_200_OK)

