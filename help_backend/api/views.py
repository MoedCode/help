from api.views_users_management import *
from api.views_groups import *
from api.views_locations import *
from api.views_subscriptions import*


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
