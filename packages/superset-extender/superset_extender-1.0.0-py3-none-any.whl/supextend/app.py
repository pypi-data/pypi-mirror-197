from flask import Flask

from supextend.config import ConfigExtenderUI
from supextend.initialization import db, bcrypt, login_manager, oidc, migrate
from supextend.utils import cli
from supextend.utils import superset
from supextend.loggers.config import LoggingConfig


def create_app(config_class=ConfigExtenderUI) -> Flask:
    from supextend.views.dashboards.routes import dashboards
    from supextend.views.workspaces.routes import workspaces
    from supextend.views.charts.routes import charts
    from supextend.views.auth.routes import auth

    app = SupersetExtenderApp(__name__)

    try:
        app.config.from_object(config_class)

        # register blueprints
        app.register_blueprint(dashboards)
        app.register_blueprint(workspaces)
        app.register_blueprint(charts)
        app.register_blueprint(auth)

        oidc.init_app(app)
        bcrypt.init_app(app)
        db.init_app(app)
        cli.init_app(app)
        login_manager.init_app(app)
        superset.csrf.init_app(app)
        migrate.init_app(app, db)
        LoggingConfig.logger.success("App created")
        return app

    except Exception as ex:
        LoggingConfig.logger.critical("Failed to create app")
        raise ex


class SupersetExtenderApp(Flask):
    pass
