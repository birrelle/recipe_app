from flask import Flask, jsonify, request
from pymongo import MongoClient, ASCENDING
from flask_cors import CORS
from app.routes import recipes_bp, users_bp, collections_bp

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

#Register Blueprints
app.register_blueprint(recipes_bp, url_prefix="/recipes")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(collections_bp, url_prefix="/collections")

#NOT SURE IF THIS DOES ANYTHING
# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Default to 500 if no specific code is set
    code = 500
    if hasattr(e, 'code'):
        code = e.code

    return jsonify({
        "message": str(e),
        "error": type(e).__name__,
        "status": code
    }), code

if __name__ == '__main__':
    app.run(debug=True)
