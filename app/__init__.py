from flask import Flask, jsonify
from app.config import config
from app.extensions import db, jwt, migrate
from flask_cors import CORS
from app.routes.upload import upload_bp
from app.routes.stream import read_bp
from app.routes.auth import auth_bp



def create_app():

    app = Flask(__name__)

    CORS(app, resources={r"/api*":{"origins":[
        "https://localhost:3000"
    ]}})
    app.config.from_object(config)
    from  app import models
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)



    app.register_blueprint(upload_bp)
    app.register_blueprint(read_bp)
    app.register_blueprint(auth_bp)
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource Not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error":"Internal server error"}), 500
    
    @app.errorhandler(403)
    def not_Authourized(e):
        return jsonify({"error":"Not authourized"}), 403
    

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error":"Bad request please send valid request"}),400
    

    return app

    
    