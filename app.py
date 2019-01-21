from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from playhouse.flask_utils import object_list

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


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/')
def index():
    entries = models.Entry.select()
    if entries:
        return object_list('index.html', entries)
    else:
        return render_template('index.html', entries=entries)


@app.route('/entry', methods=('GET', 'POST'))
@login_required
def entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            user=g.user._get_current_object(),
            slug=form.slug.data,
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            subjects=form.subjects.data.strip(),
            resources=form.resources.data.strip()
            )
        flash('Entry created!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username=config.DEFAULT_USER,
            email=config.DEFAULT_USER_EMAIL,
            password=config.DEFAULT_USER_PASSWORD,
        )
    except ValueError:
        pass

    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
