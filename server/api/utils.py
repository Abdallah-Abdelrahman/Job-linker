""" Utils for the flask app """

from flask import jsonify


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
    return jsonify({"status": status, "message": message, "data": data})
