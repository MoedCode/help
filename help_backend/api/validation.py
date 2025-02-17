
import re
from datetime import date
from django.core.exceptions import ValidationError
from api.models import Users  # Import the Users model


def validate_user_data(request_data):
    """
    Validates user data from the request before creating a Users instance.
    - Ensures only valid fields are provided.
    - Validates required fields and data format.
    """

    # Get all valid field names from the Users model (excluding inherited ones)
    valid_fields = {field.name for field in Users._meta.get_fields() if not field.is_relation}

    # Check for extra keys in request data
    extra_keys = set(request_data.keys()) - valid_fields
    if extra_keys:
        raise ValidationError({"extra_keys": f"Invalid fields found: {', '.join(extra_keys)}"})

    # Check for missing required fields
    required_fields = {"email", "first_name", "last_name", "mobile_number"}
    missing_fields = required_fields - request_data.keys()
    if missing_fields:
        raise ValidationError({"missing_fields": f"Missing required fields: {', '.join(missing_fields)}"})

    # Validate mobile number (only digits, 10-15 characters)
    mobile_number = request_data.get("mobile_number", "")
    if not re.fullmatch(r"^\d{10,15}$", mobile_number):
        raise ValidationError({"mobile_number": "Mobile number must be between 10 to 15 digits and contain only digits."})

    # Validate date of birth (if provided, user must be at least 13 years old)
    date_of_birth = request_data.get("date_of_birth")
    if date_of_birth:
        try:
            dob = date.fromisoformat(date_of_birth)  # Ensure it's in "YYYY-MM-DD" format
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 13:
                raise ValidationError({"date_of_birth": "User must be at least 13 years old."})
        except ValueError:
            raise ValidationError({"date_of_birth": "Invalid date format. Use 'YYYY-MM-DD'."})

    # Validate address fields (if provided, they cannot be empty strings)
    for field in ["address_street", "address_city", "address_country"]:
        if field in request_data and not request_data[field].strip():
            raise ValidationError({field: f"{field.replace('_', ' ').capitalize()} cannot be empty."})

    return request_data  # Return cleaned data if valid
