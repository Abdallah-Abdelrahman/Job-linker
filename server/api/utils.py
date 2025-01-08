"""Utils for the flask app"""

from flask import Response, json, jsonify

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
    response = {
            "status": status,
            "message": message,
            "data": data
        }
        
    return Response(
        json.dumps(response, ensure_ascii=False),  # ensure_ascii=False to handle Arabic
        content_type="application/json"
    )
