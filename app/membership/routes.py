import os
from flask.helpers import flash
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for
from config import Config as config

from .. import db
from ..utils.mail import send_membership_mail
from .forms import PaymentForm

bp = Blueprint("membership", __name__)

@bp.route('/membership')
def pricing():
    # if the user is logged in or not
    user = current_user if current_user.is_authenticated else None

    # prices static for now to fetched from db later
    prices = [
        {
            'title': 'Basic',
            'value': 7000,
            'benifits': [
                '3 day stay at Mandalpatti Resort',
                '',
                ''
            ]
        },
        {
            'title': 'Gold',
            'value': 10000,
            'benifits': [
                '3 day stay at Mandalpatti Resort',
                'Tours and Trekking',
                ''
            ]
        },
        {
            'title': 'Platinum',
            'value': 15000,
            'benifits': [
                '3 day stay at Mandalpatti Resort',
                'Tours and Trekking',
                'Spa Facilities'
            ]
        }
    ]
    return render_template('membership.html', current_user=user, prices=prices)


@bp.route('/payment/<string:membership_type>', methods=["GET", "POST"])
@login_required
def payment(membership_type):
    form = PaymentForm()
    if form.validate_on_submit():
        # save the photo for id card
        file_path = os.path.join(os.getcwd(), config.UPLOAD_DIR, "{}_{}.jpg".format(current_user.username, current_user.id))
        form.photo.data.save(file_path)

        # update user membership
        current_user.is_member = True
        current_user.membership_type = membership_type
        db.session.commit()
        
        # send mebership mail
        # send_membership_mail(current_user, file_path)

        flash('Congratulations you are now a member!')
        return redirect(url_for('dashboard.index'))

    return render_template('payment.html', current_user=current_user, form=form)