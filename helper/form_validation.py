"""Helper to validate form request required"""
from flask import request, jsonify
from werkzeug.exceptions import BadRequest


def get_form_data(required_fields, request):
    """
    Extracts form data and performs basic validation.

    Args:
        required_fields (list): A list of strings representing the required form fields.

    Returns:
        dict: A dictionary containing the extracted form data or raises a BadRequest exception.

    Raises:
        BadRequest: If any required field is missing or empty.
    """

    data = {}
    for field in required_fields:
        # coba ambil dari form dulu
        field_value = request.form.get(field)
        if field_value is None:
            # kalau tidak ada di form, coba dari files
            field_value = request.files.get(field)
        
        if field_value is None or (hasattr(field_value, 'filename') and field_value.filename == ''):
            err_message = jsonify({"err_message": f"Missing required field: {field}"})
            raise BadRequest(response=err_message)

        data[field] = field_value
    return data
