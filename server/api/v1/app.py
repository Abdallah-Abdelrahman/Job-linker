"""
This module sets up the Flask application for the Job-linker application.
"""
import os
import redis
from server.models import storage
from server.error_handlers import register_error_handlers
from server.extensions import app, jwt
from server.jwt_handlers import register_jwt_handlers
from dotenv import load_dotenv


load_dotenv()

redis_host = os.environ['REDIS_HOST']
redis_port = int(os.environ['REDIS_PORT'])
redis_db_jwt = int(os.environ['REDIS_DB_JWT'])

jwt_redis_blocklist = redis.StrictRedis(
        host=redis_host, port=redis_port, db=redis_db_jwt, decode_responses=True
        )

def create_app():
    """
    Initializes the Flask application.

    Sets up error handlers, JWT handlers, and blueprints.
    """
    # Setup our redis connection for storing the blocklisted tokens. You will probably
    # want your redis instance configured to persist data to disk, so that a restart
    # does not cause your application to forget that a JWT was revoked.
    from server.api.v1.views import app_views

    register_error_handlers(app)
    register_jwt_handlers(jwt)


    app.register_blueprint(app_views)


    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        '''Callback function to check if a JWT exists in the redis blocklist'''
        jti = jwt_payload.get("jti")
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Close the database session at the end of the request."""
        storage.close()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=False, threaded=True)
