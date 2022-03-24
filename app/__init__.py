"""Initialize Flask app."""
from flask import Flask
import os


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = os.urandom(24)
    # app.config['UPLOAD_EXTENSIONS'] = ['.xlsx', '.csv']
    # app.config.from_object('config.Config')
    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        # Import Dash application (connecting dash to flask)
        from .intro.intro import init_dashboard
        app = init_dashboard(app)

        from .aa.aa import init_dashboard
        app = init_dashboard(app)

        from .psmaa.psmaa import init_dashboard
        app = init_dashboard(app)

        from .sa.sa_insta import init_dashboard
        app = init_dashboard(app)

        from .sa.sa_fb import init_dashboard
        app = init_dashboard(app)

        from .ia.ia import init_dashboard
        app = init_dashboard(app)

        return app
