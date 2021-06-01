# coding=utf-8

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from flask import current_app
import rq
import redis
import sys


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    submissions = db.relationship('Submission', backref='user', lazy=True)

class Submission(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(5000), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    date_submitted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.PickleType)
    times = db.Column(db.PickleType)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    tasks = db.relationship('Task', backref='submission', lazy='dynamic')

    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name,
                                                *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description,
                    submission=self)
        db.session.add(task)
        db.session.commit()
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(submission=self, complete=False).all()

    def get_task_in_progress(self):
        return Task.query.filter_by(submission=self,
                                    complete=False).first()

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
