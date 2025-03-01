from api.views_users_management import *
from api.views_groups import *
from api.views_locations import *
from api.views_subscriptions import*

# from twilio.rest import Client

from .utils import send_sms

class SendSMSView(APIView):
    def post(self, request):
        to_phone_number = request.data.get('to_phone_number')
        message = request.data.get('message')

        if not to_phone_number or not message:
            return Response(
                {"error": "Both 'to_phone_number' and 'message' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = send_sms(to_phone_number, message)

        if result["status"] == "success":
            return Response({"status": "success", "message_sid": result["message_sid"]}, status=status.HTTP_200_OK)
        else:
            return Response({"error": result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import logging
from django.core.mail import send_mail
logger = logging.getLogger(__name__)

class SendEmailToTest(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Send a POST request to send an email"}, status=200)
    def post(self, request):
        try:
            print("\na7a7a7a -1")
            # Extract email details from request
            dist_mail = request.data.get("dist_mail", "").strip()
            dist_mail_body = request.data.get("dist_mail_body", "").strip()
            dist_mail_sub = request.data.get("dist_mail_sub", "").strip()
            print("\na7a7a7a -2")

            if not dist_mail or not dist_mail_body or not dist_mail_sub:
                return Response({"error": "All fields are required (dist_mail, dist_mail_body, dist_mail_sub)"}, status=400)

            # Sending email
            x = send_mail(
                subject=dist_mail_sub,
                message=dist_mail_body,
                from_email='coolkatsumi@gmail.com',
                recipient_list=[dist_mail],
                fail_silently=False  # Ensures errors are raised for debugging
            )
            print("\na7a7a7a -3")

            logger.info(f"Email sent successfully to {dist_mail}")
            print("\na7a7a7a -4")

            return Response({"success": bool(x)}, status=200)

        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return Response({"error": str(e)}, status=500)
dataDict ={
"dist_mail":"sirmohamedh@gmail.com",
"dist_mail_body":"email body 4 test ",
"dist_mail_sub":"email subject 4 test "
}
req = {"data":dataDict}
s= SendEmailToTest()
m = s.post(req)
print(f"\n\n\n{m}\n\n\n")

# class SendSMS:
#     def __init__(self, account_sid, auth_token, twilio_number):
#         self.client = Client(account_sid, auth_token)
#         self.twilio_number = twilio_number

#     def send(self, receiver_number, message):
#         try:
#             msg = self.client.messages.create(
#                 body=message,
#                 from_=self.twilio_number,
#                 to=receiver_number
#             )
#             return True, f"SMS sent to {receiver_number} (SID: {msg.sid})"
#         except Exception as e:
#             return False, f"Error: {str(e)}"
# # send_sms =  SendSMS()
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
            msg = "";
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
                    msg +=": " + help_msg if help_msg else "help"
                # else:

                    # send_sms.send(member.mobile_number, sms)
                # if help_msg:
                #     member_data["message"] = help_msg

                members_data.append(member_data)
            for _ in members_data:
                if not _["sender"]:
                    _["help_message"] = msg
                    del _["sender"]
                else:
                    members_data.remove(_)

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
