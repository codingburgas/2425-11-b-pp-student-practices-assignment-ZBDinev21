from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        current_user.username = request.form['username']
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('profile.edit'))
    return render_template('edit_profile.html', user=current_user)
