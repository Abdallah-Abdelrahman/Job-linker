"""
This module sets up the Flask application for the Job-linker application.
"""
import redis
from server.error_handlers import register_error_handlers
from server.extensions import app, jwt
from server.jwt_handlers import register_jwt_handlers


jwt_redis_blocklist = redis.StrictRedis(
        host="localhost", port=6379, db=0, decode_responses=True
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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
