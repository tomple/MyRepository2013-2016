from flask import Flask, current_app, redirect, url_for, request
import flask_login
import logging

loghandler = logging.FileHandler('flask.log')
logging_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(lineno)s]: %(message)s')
loghandler.setFormatter(logging_format)
login_manager = flask_login.LoginManager()
login_manager.login_view = 'main.login'


def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.config.update(dict(DEBUG=True, SECRET_KEY='development key'))
    app.logger.addHandler(loghandler)

    @app.errorhandler(404)
    @app.errorhandler(401)
    @flask_login.login_required
    def page_not_found(e):
        current_app.logger.info('%s:%s [open_errorhandler]' % (flask_login.current_user.id, request.url))
        return redirect(url_for('main.uploadfile'))

    return app
