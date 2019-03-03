import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SERVER_NAME='lvh.me:5000',
        DATABASE=os.path.join(app.instance_path, 'teams.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import teams
    app.register_blueprint(teams.bp)

    from . import brokenteams
    app.register_blueprint(brokenteams.bp)
    
    from . import image
    app.register_blueprint(image.bp)
    
    from . import badimage
    app.register_blueprint(badimage.bp)
    
    return app

