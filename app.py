from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import config
import models
import forms


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
# Initiate Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """
    Connect to the database befora eash request
    """
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """
    Close db after each request
    """
    g.db.close()
    return response


@app.route('/')
def index():
    return "Hello"


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='ismail',
            email='iaksoy@seanapse.io',
            password='password',
            admin=True
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)
