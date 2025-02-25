from api.views_users_management import *
from api.views_groups import *
from api.views_locations import *
from api.views_subscriptions import*

from twilio.rest import Client


class SendSMS:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number

    def send(self, receiver_number, message):
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.twilio_number,
                to=receiver_number
            )
            return True, f"SMS sent to {receiver_number} (SID: {msg.sid})"
        except Exception as e:
            return False, f"Error: {str(e)}"
# send_sms =  SendSMS()
class SendHelpToGroupMembers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, msg=""):
        if msg:
            request.data["message"] = msg
        return Response(self.members_data(request), S200)
    def post(self, request):

        return Response(self.members_data(request), S200)


    @classmethod
    def members_data(cls, request):
        try:
            sms = "";
            help_msg = request.data.get("message", "")
            # return {"user":request.user.username}
            group = Groups.objects.filter(members=request.user).first()
            members = list(group.members.all());
            members_data = []
            for member in members:
                member_data = {
                    "name":GroupContact.objects.filter(user=member).first().contact_name,
                    "mobile_number": member.mobile_number,
                    "email": member.email,
                    "sender":False
                }
                if request.user.id == member.id:
                    member_data["sender"] = True
                    msg = f"{member_data['name']} is sending"
                    msg += help_msg if help_msg else "help"
                    member_data["sms"] = msg
                # else:

                    # send_sms.send(member.mobile_number, sms)
                # if help_msg:
                #     member_data["message"] = help_msg
                members_data.append(member_data)
            return members_data
        except Exception as e:
            return {"error":str(e)}


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
