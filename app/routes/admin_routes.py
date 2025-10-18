from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import Module, Question, Badge, User, db
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# --------------------------
# Decorator for admin access
# --------------------------
def admin_required(view_func):
    @login_required
    def wrapped_view(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admin access only.")
            return redirect(url_for('user.dashboard'))
        return view_func(*args, **kwargs)
    wrapped_view.__name__ = view_func.__name__
    return wrapped_view


# --------------------------
# Admin Home
# --------------------------
@admin_bp.route('/')
@admin_required
def admin_home():
    total_users = User.query.count()
    total_modules = Module.query.count()
    total_badges = Badge.query.count()
    total_questions = Question.query.count()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_modules=total_modules,
        total_badges=total_badges,
        total_questions=total_questions
    )


# --------------------------
# Manage Modules
# --------------------------
@admin_bp.route('/modules')
@admin_required
def manage_modules():
    modules = Module.query.all()
    return render_template('admin/modules.html', modules=modules)


@admin_bp.route('/modules/add', methods=['GET', 'POST'])
@admin_required
def add_module():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')  # <-- Make sure this line exists

        new_module = Module(title=title, description=description, content=content)  # <-- Include content
        db.session.add(new_module)
        db.session.commit()
        flash('Module added successfully!', 'success')
        return redirect(url_for('admin.manage_modules'))
    return render_template('admin/add_module.html')


@admin_bp.route('/modules/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_module(id):
    module = Module.query.get_or_404(id)
    if request.method == 'POST':
        module.title = request.form.get('title')
        module.description = request.form.get('description')
        module.content = request.form.get('content')  # <-- Make sure this line is present!
        db.session.commit()
        flash('Module updated successfully!', 'success')
        return redirect(url_for('admin.manage_modules'))
    return render_template('admin/edit_module.html', module=module)


@admin_bp.route('/modules/delete/<int:id>', methods=['POST'])
@admin_required
def delete_module(id):
    module = Module.query.get_or_404(id)
    db.session.delete(module)
    db.session.commit()
    flash('Module deleted.')
    return redirect(url_for('admin.manage_modules'))


# --------------------------
# Manage Questions (per module)
# --------------------------
@admin_bp.route('/modules/<int:module_id>/questions')
@admin_required
def manage_questions(module_id):
    module = Module.query.get_or_404(module_id)
    questions = Question.query.filter_by(module_id=module_id).all()
    return render_template('admin/questions.html', module=module, questions=questions)


@admin_bp.route('/modules/<int:module_id>/questions/add', methods=['GET', 'POST'])
@admin_required
def add_question(module_id):
    module = Module.query.get_or_404(module_id)
    if request.method == 'POST':
        options = {
            "A": request.form['option_a'],
            "B": request.form['option_b'],
            "C": request.form['option_c'],
            "D": request.form['option_d']
        }

        q = Question(
            module_id=module_id,
            text=request.form['question_text'],
            options=json.dumps(options),
            correct_option=request.form['correct_option']
        )
        db.session.add(q)
        db.session.commit()
        flash('Question added successfully.')
        return redirect(url_for('admin.manage_questions', module_id=module_id))
    return render_template('admin/add_question.html', module=module)


@admin_bp.route('/questions/edit/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    options = json.loads(question.options)

    if request.method == 'POST':
        question.text = request.form['question_text']
        new_options = {
            "A": request.form['option_a'],
            "B": request.form['option_b'],
            "C": request.form['option_c'],
            "D": request.form['option_d']
        }
        question.options = json.dumps(new_options)
        question.correct_option = request.form['correct_option']
        db.session.commit()
        flash('Question updated.')
        return redirect(url_for('admin.manage_questions', module_id=question.module_id))
    return render_template('admin/edit_question.html', question=question, options=options)


@admin_bp.route('/questions/delete/<int:question_id>', methods=['POST'])
@admin_required
def delete_question(question_id):
    q = Question.query.get_or_404(question_id)
    module_id = q.module_id
    db.session.delete(q)
    db.session.commit()
    flash('Question deleted.')
    return redirect(url_for('admin.manage_questions', module_id=module_id))


# ✅ --------------------------
# NEW: Manage All Questions (for Dashboard link)
# --------------------------
@admin_bp.route('/questions')
@admin_required
def manage_all_questions():
    questions = Question.query.all()
    modules = {m.id: m.title for m in Module.query.all()}
    return render_template('admin/all_questions.html', questions=questions, modules=modules)


# --------------------------
# Manage Badges
# --------------------------
@admin_bp.route('/badges')
@admin_required
def badges():
    badges = Badge.query.all()
    return render_template('admin/badges.html', badges=badges)


@admin_bp.route('/badges/add', methods=['GET', 'POST'])
@admin_required
def add_badge():
    modules = Module.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        criteria = request.form.get('criteria')
        module_id = request.form.get('module_id')
        badge = Badge(name=name, description=description, criteria=criteria, module_id=module_id)
        db.session.add(badge)
        db.session.commit()
        flash('Badge added successfully!', 'success')
        return redirect(url_for('admin.badges'))
    return render_template('admin/add_badge.html', modules=modules)


@admin_bp.route('/badges/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_badge(id):
    badge = Badge.query.get_or_404(id)
    if request.method == 'POST':
        badge.name = request.form['name']
        badge.description = request.form['description']
        badge.criteria = request.form['criteria']
        db.session.commit()
        flash('Badge updated.')
        return redirect(url_for('admin.badges'))  # <-- FIXED
    return render_template('admin/edit_badge.html', badge=badge)


@admin_bp.route('/badges/delete/<int:id>', methods=['POST'])
@admin_required
def delete_badge(id):
    badge = Badge.query.get_or_404(id)
    db.session.delete(badge)
    db.session.commit()
    flash('Badge deleted.')
    return redirect(url_for('admin.badges'))  # <-- FIXED

# recent_modules = [Module.query.get(p.module_id) for p in recent_progress if Module.query.get(p.module_id) is not None]
