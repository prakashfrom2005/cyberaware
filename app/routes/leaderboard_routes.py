from flask import Blueprint, render_template
from ..models import User
from flask_login import current_user


leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@leaderboard_bp.route('/')
def leaderboard():
    users = User.query.filter_by(is_admin=False).order_by(User.points.desc()).all()
    return render_template('leaderboard/view.html', users=users, current_user=current_user)
