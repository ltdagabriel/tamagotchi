from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from route import route
from flask_debug import Debug
import os


def create_app(configfile=None):
    # We are using the "Application Factory"-pattern here, which is described
    # in detail inside the Flask docs:
    # http://flask.pocoo.org/docs/patterns/appfactories/

    app = Flask(__name__)

    app.secret_key = os.urandom(12)
    Debug(app)
    # We use Flask-Appconfig here, but this is not a requirement
    AppConfig(app)
    # Install our Bootstrap extension
    Bootstrap(app)

    # Our application uses blueprints as well; these go well with the
    # application factory. We already imported the blueprint, now we just need
    # to register it:
    app.register_blueprint(route)

    # Because we're security-conscious developers, we also hard-code disabling
    # the CDN support (this might become a default in later versions):
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='localhost', port=5000)
