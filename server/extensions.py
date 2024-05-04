"""
Job Linker Flask app configuration
"""

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from server.config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.url_map.strict_slashes = False
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

swagger = Swagger(app)
jwt = JWTManager(app)
