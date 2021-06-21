from flask_login import login_user, logout_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from .models import User
from .. import login_manager, db
from .forms import LoginForm, CreateAccountForm, ForgotPasswordForm, ResetPassswordForm
from ..utils.mail import send_reset_email, send_registration_mail

bp = Blueprint("user", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        # Locate user
        user = User.query.filter_by(email=data['email']).first()

        # Check the password
        if user and user.check_password(data['password']):
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            # Something (user or pass) is not ok
            flash('Invalid Credentials')
            redirect(url_for('user.login'))
    return render_template( 'login.html', form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = CreateAccountForm()
    if form.validate_on_submit():
        data = form.data
        del data['csrf_token']

        # Check email exists
        user = User.query.filter_by(email=data['email']).first()
        if user:
            form = CreateAccountForm()
            flash('Email already registered')
            return redirect(url_for('user.register'))

        # else we can create the user
        user = User(**data)
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        # sending registration email
        # send_registration_mail(user)

        login_user(user)

        return redirect(url_for('dashboard.index'))
    return render_template("register.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    # logout a user
    logout_user()
    form = LoginForm()
    return redirect(url_for('user.login'))

@bp.route("/forgotpassword", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        form = ForgotPasswordForm()
        return render_template("forgotpassword.html", form=form)
    else:
        email = request.form['email']

        form=ForgotPasswordForm()

        user = User.query.filter_by(email = email).first()
        if not user:
            return render_template("forgotpassword.html", form=form, msg="Email not found")

        # Send reset email to the user
        send_reset_email(user)

        return render_template("forgotpassword.html", msg="Reset link has been sent to your email id", form=form)


@bp.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "GET":
        form = ResetPassswordForm()
        return render_template("resetpassword.html", form=form, token=token)
    else:
        user = User.verify_reset_token(token)
        if not user:
            return redirect(url_for('user.login'))

        user.set_password(request.form['password'])
        db.session.commit()

        return redirect(url_for('user.login'))


## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('user.login'))
