""" Utils for the flask app """

from flask import Response, json, jsonify


def make_response_(status, message, data=None):
    """
    Creates a unified response format.

    Args:
        status (str): The status of the response.
        message (str): The message to be included in the response.
        data (dict, optional): Any additional data to be included
        in the response.

    Returns:
        dict: The response dictionary.
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
