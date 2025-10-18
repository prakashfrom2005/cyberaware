from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Module, Question, UserProgress, db
from ..models import Badge, UserBadge, QuizAttempt
from datetime import date, timedelta, datetime
import json

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')


@quiz_bp.route('/<int:module_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(module_id):
    module = Module.query.get_or_404(module_id)
    questions = Question.query.filter_by(module_id=module_id).all()

    if not questions:
        flash("No questions found for this module. Quiz is unavailable.")
        return redirect(url_for('module.view_module', module_id=module_id))

    for q in questions:
        try:
            raw_choices = json.loads(q.options)
            q.choices = [f"{key}) {value}" for key, value in raw_choices.items()]
        except Exception as e:
            q.choices = []
            print(f"Error decoding options for question {q.id}: {e}")

    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.form.get(f'q{q.id}')
            if selected:
                selected_letter = selected.split(")")[0].strip().upper()
                if selected_letter == q.correct_option.upper():
                    score += 1

        percent = round((score / len(questions)) * 100)

        # Store the quiz attempt
        new_attempt = QuizAttempt(
            user_id=current_user.id,
            module_id=module_id,
            score=percent,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_attempt)

        progress = UserProgress.query.filter_by(user_id=current_user.id, module_id=module_id).first()
        if not progress:
            progress = UserProgress(user_id=current_user.id, module_id=module_id)

        progress.score = percent
        progress.completed = True
        progress.completed_on = datetime.utcnow()
        db.session.add(progress)

        all_scores = UserProgress.query.filter_by(user_id=current_user.id).all()
        current_user.points = sum(p.score for p in all_scores)
        current_user.level = current_user.points // 100 + 1

        today = date.today()
        last = UserProgress.query.filter_by(user_id=current_user.id).order_by(UserProgress.completed_on.desc()).first()

        if last and last.completed_on:
            last_date = last.completed_on.date()
            if last_date == today - timedelta(days=1):
                current_user.streak += 1
            elif last_date != today:
                current_user.streak = 1
        else:
            current_user.streak = 1

        earned_badges = []
        eligible_badges = Badge.query.filter_by(module_id=module_id).all()

        # Extract the numeric value from criteria and sort badges descending
        def get_criteria_value(badge):
            # Assumes criteria is like "score >= 80"
            try:
                return int(''.join(filter(str.isdigit, badge.criteria)))
            except:
                return 0

        eligible_badges = sorted(eligible_badges, key=get_criteria_value, reverse=True)

        for badge in eligible_badges:
            condition = badge.criteria.replace("score", str(percent))
            if eval(condition):
                existing = UserBadge.query.filter_by(user_id=current_user.id, badge_id=badge.id).first()
                if not existing:
                    earned = UserBadge(user_id=current_user.id, badge_id=badge.id)
                    db.session.add(earned)
                    earned_badges.append(badge)
                break  # Stop after awarding the highest badge

        db.session.commit()

        return render_template(
            'quiz/quiz_result.html',
            module=module,
            percent=percent,
            earned_badges=earned_badges
        )

    return render_template('quiz/take_quiz.html', module=module, questions=questions)
