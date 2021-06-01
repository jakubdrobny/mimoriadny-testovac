from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from app import db, bcrypt
from app.users.forms import RegistrationForm, LoginForm, UpdateProfileForm
from app.models import User
import sys

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Už si prihlásený.', 'warning')
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Tvoj účet bol vytvorený! Môžeš sa prihlásiť.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Registrácia', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Už si prihlásený.', 'warning')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Prihlásenie neúspešné. Prosím, skontroluj si meno a heslo.', 'danger')
    return render_template('login.html', title='Prihlasovanie', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash('Bol si úspešne odhlásený.', 'success')
    return redirect(url_for('main.home'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tvoj profil bol úspešne upravený.', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', title=f'{current_user.username} - Profile', form=form)