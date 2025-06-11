from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models import User, SurveyResponse
from app.extensions import db

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.before_request
def restrict_to_admin():
    if session.get('role') != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('main.home'))

@admin_bp.route('/')
def dashboard():
    users = User.query.all()
    surveys = SurveyResponse.query.order_by(SurveyResponse.created_at.desc()).all()
    return render_template('dashboard.html', users=users, surveys=surveys)

@admin_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'info')
    return redirect(url_for('admin.dashboard'))
