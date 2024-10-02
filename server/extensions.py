"""
Job Linker Flask app configuration
"""

from flasgger import Swagger
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

from server.config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

app.url_map.strict_slashes = False
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://job-linker.netlify.app"}}, expose_headers=["Content-Type", "Authorization"])

swagger = Swagger(app)
jwt = JWTManager(app)
cache = Cache(app)

# Redis configuration for JWT revoking
redis_host = app.config['REDIS_HOST']
redis_port = app.config['REDIS_PORT']
redis_db_jwt = app.config['REDIS_DB_JWT']

# Redis connection for JWT revoking
jwt_redis_connection = Redis(host=redis_host, port=redis_port, db=redis_db_jwt)

# Redis configuration for rate limiter
redis_db_limiter = app.config['REDIS_DB_LIMITER']

# Redis connection for rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=f"redis://{redis_host}:{redis_port}/{redis_db_limiter}",
    default_limits=["200 per day", "50 per hour"],
)

swagger.config["title"] = "Job Linker API"
swagger.config["version"] = "0.0.1"
swagger.config[
        "description"
        ] = "API End-points to interact with the application"
