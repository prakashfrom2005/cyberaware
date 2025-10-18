from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Module, UserProgress

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    completed = UserProgress.query.filter_by(user_id=current_user.id, completed=True).count()
    total = Module.query.count()
    progress_percent = round((completed / total) * 100) if total else 0

    recent_progress = (
        UserProgress.query
        .filter_by(user_id=current_user.id, completed=True)
        .order_by(UserProgress.completed_on.desc())
        .limit(5)
        .all()
    )
    # avoid calling Module.query.get(None) which raises SAWarning
    recent_modules = []
    for p in recent_progress:
        if p.module_id is None:
            continue
        m = Module.query.get(p.module_id)
        if m:
            recent_modules.append(m)

    streak = getattr(current_user, "streak", 0)  # Assuming you store streak on the user model

    return render_template(
        'user/dashboard.html',
        completed=completed,
        total=total,
        progress_percent=progress_percent,
        recent_modules=recent_modules,
        streak=streak
    )
