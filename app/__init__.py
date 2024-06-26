from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ffa2392d1d4bcb5b37e79f253cd250573c4fd3730d7156d6'

    from .routes import main
    app.register_blueprint(main)

    return app
