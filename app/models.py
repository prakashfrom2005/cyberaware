from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak = db.Column(db.Integer, default=0)
    badges = db.relationship('UserBadge', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    questions = db.relationship('Question', backref='module', cascade='all, delete-orphan')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    options = db.Column(db.String(500), nullable=False)  # JSON string
    correct_option = db.Column(db.String(100), nullable=False)


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    completed_on = db.Column(db.DateTime, default=datetime.utcnow)
    module = db.relationship('Module', backref='progress_records')


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    criteria = db.Column(db.String(255), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)  # <-- Add this line

    module = db.relationship('Module', backref='badges')


class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'))
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)
    badge = db.relationship('Badge', backref='user_badges')


class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # DO NOT add unique=True to user_id/module_id together!


User.badges = db.relationship('UserBadge', backref='user', lazy=True)
