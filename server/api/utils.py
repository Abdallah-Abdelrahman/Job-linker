"""Utils for the flask app"""

from flask import jsonify, make_response

def make_response_(status, message, data=None, cookies=None):
    """
    Creates a unified response format and sets cookies if provided.

    Args:
        status (str): The status of the response.
        message (str): The message to be included in the response.
        data (dict, optional): Any additional data to be included
        in the response.
        cookies (dict, optional): A dictionary of cookies to be set
        in the response.

    Returns:
        Response: The response object.
    """
    if data is None:
        data = {}
    response = make_response(jsonify({"status": status, "message": message, "data": data}))
    
    # Set cookies if provided
    if cookies:
        for cookie_name, cookie_value in cookies.items():
            response.set_cookie(cookie_name, cookie_value['value'], httponly=True, samesite='None', secure=True, max_age=cookie_value.get('max_age'))
    
    return response
