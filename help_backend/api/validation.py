
import re
from datetime import date
from django.core.exceptions import ValidationError
from api.models import Users  # Import the Users model
import pycountry
from geopy.geocoders import Nominatim
from rest_framework.exceptions import ValidationError
import pycountry
from geopy.geocoders import Nominatim

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
    required_fields = {"email", "first_name", "last_name", "mobile_number", "password"}
    missing_fields = required_fields - request_data.keys()
    if missing_fields:
        raise ValidationError({"missing_fields": f"Missing required fields: {', '.join(missing_fields)}"})

    # Validate password (must be at least 8 characters)
    password = request_data.get("password", "")
    if len(password) < 8:
        raise ValidationError({"password": "Password must be at least 8 characters long."})

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
    for field in ["street", "city", "country"]:
        if field in request_data and not request_data[field].strip():
            raise ValidationError({field: f"{field.replace('_', ' ').capitalize()} cannot be empty."})

    return request_data  # Return cleaned data if valid
def validate_profile_update(data):
    """
    Validate and filter profile update data.

    - Keeps only allowed keys.
    - Ensures correct data types.
    - Returns (True, valid_data) if valid.
    - Returns (False, errors) if there are invalid fields.
    """

    # Allowed keys and their expected types
    allowed_keys = {
        "bio": str,
        "profile_image": (str, bytes),  # Accept file path or binary image data
        "profession": str,
        "location": str,
        "verified": bool,
    }

    valid_data = {}
    errors = {}

    for key, value in data.items():
        if key in allowed_keys:
            # Check if value matches expected type
            if isinstance(value, allowed_keys[key]):
                valid_data[key] = value
            else:
                errors[key] = f"Expected {allowed_keys[key]}, got {type(value).__name__}."
        else:
            errors[key] = "Invalid field."

    # If errors exist, return False with error messages
    if errors:
        return False, errors

    return True, valid_data  # If everything is valid, return True with filtered data



import pycountry
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut, GeocoderQuotaExceeded

def validate_location(data):
    """
    Validate that the location data contains all required fields,
    ensures the city exists and belongs to the given country,
    and checks for valid latitude and longitude values.

    Returns:
        (True, validated_data) if valid
        (False, error_messages) if invalid
    """
    required_fields = ["city", "country", "latitude", "longitude"]
    errors = {}

    # Check if all required fields are present
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f"{field} is required."

    if errors:
        return False, errors

    city = data["city"].strip()
    country = data["country"].strip()
    latitude = data["latitude"]
    longitude = data["longitude"]

    # Validate latitude and longitude ranges
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        if not (-90 <= latitude <= 90):
            errors["latitude"] = "Latitude must be between -90 and 90."
        if not (-180 <= longitude <= 180):
            errors["longitude"] = "Longitude must be between -180 and 180."
    except ValueError:
        errors["latitude"] = "Latitude must be a valid number."
        errors["longitude"] = "Longitude must be a valid number."

    # Validate that the country exists (by name or ISO alpha-2)
    country_obj = pycountry.countries.get(name=country) or pycountry.countries.get(alpha_2=country.upper())
    if not country_obj:
        errors["country"] = "Invalid country name or code."

    if errors:
        return False, errors

    # Validate that the city exists in the given country
    geolocator = Nominatim(user_agent="your_unique_app_name", timeout=10)
    try:
        location = geolocator.geocode(f"{city}, {country_obj.name}", exactly_one=True)
        if not location:
            errors["city"] = f"Could not find {city} in {country_obj.name}."
    except GeocoderQuotaExceeded:
        errors["geocode"] = "Geocoder rate limit exceeded. Try again later."
    except (GeocoderServiceError, GeocoderTimedOut):
        errors["geocode"] = "Geolocation service unavailable or request timed out."

    if errors:
        return False, errors

    # If all validations pass
    validated_data = {
        "city": city,
        "country": country_obj.name,
        "latitude": latitude,
        "longitude": longitude
    }
    return True, validated_data


