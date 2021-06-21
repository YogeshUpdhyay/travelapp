from app.main.models import Events
from flask import Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_required
import os

from .. import login_manager, db
from ..utils.mail import send_event_mail
from .models import *

bp = Blueprint("dashboard", __name__)

@bp.route("/")
def index():
    # if the user is logged in or not
    user = current_user if current_user.is_authenticated else None

    # events and feeds
    events = Events.query.limit(3).all()
    feeds = Feeds.query.limit(3).all()
 
    return render_template('index.html', current_user=user, feeds=feeds, events=events)

@bp.route('/joinevent/<int:id>')
@login_required
def join_event(id):
    # sends the email invite for the event
    event = Events.query.filter_by(id = id).first()
    send_event_mail(current_user, event)

    flash("Thank you for joining the event!")
    return redirect(url_for('dashboard.index'))

@login_required
@bp.route('/share')
def share_event():
    pass


