from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__, url_prefix='/auth')

#app/auth/routes.py

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'warning')
            return render_template('auth/register.html', form=form)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    # Debug: show validation errors when a POST fails validation
    if request.method == 'POST' and form.errors:
        errs = "; ".join(f"{f}: {', '.join(e)}" for f, e in form.errors.items())
        current_app.logger.debug("Registration form errors: %s", errs)
        flash(f"Registration error: {errs}", "danger")


    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next') or url_for('main.index')
            return redirect(next_page)
        else:
            flash('Login failed. Check username and password.', 'danger')

    if request.method == 'POST' and form.errors:
        errs = "; ".join(f"{f}: {', '.join(e)}" for f, e in form.errors.items())
        current_app.logger.debug("Login form errors: %s", errs)
        flash(f"Login error: {errs}", "danger")

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))