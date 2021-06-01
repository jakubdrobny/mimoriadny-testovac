from flask import render_template, Blueprint, abort, flash, redirect, url_for, request
from flask_login import current_user, login_required
from markdown import markdown
from app import db
from app.tasky.forms import SubmitTaskForm
from app.models import Submission
from app.utils.get_task import get_tasks, get_task_content, get_task_info, get_task_files
import sys, os, json

tasky = Blueprint('tasky', __name__)


@tasky.route('/tasks')
def tasks():
    cwd = os.getcwd() + '/ulohy'
    tasks = os.listdir(cwd)
    titles = []
    for task in tasks:
        with open(cwd + "/" + task + "/spec.json", 'r', encoding='utf-8') as f:
            task_info = json.load(f)
            titles.append(task_info['title'])
    is_admin = True if current_user.is_authenticated and current_user.username == 'jakubd' and current_user.email == 'jkubeing@gmail.com' else False
    return render_template('tasks.html', tasks=tasks, titles=titles, is_admin=is_admin)


@tasky.route('/task/<task_id>')
def task(task_id):
    if task_id not in get_tasks():
        abort(404)
    is_admin = True if current_user.is_authenticated and current_user.username == 'jakubd' and current_user.email == 'jkubeing@gmail.com' else False
    task = get_task_info(task_id)
    return render_template('task.html', task=task, content=markdown(get_task_content(task_id), extensions=['mdx_math']), is_admin=is_admin, statement=True)

@tasky.route('/task/<task_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_task(task_id):
    if task_id not in get_tasks():
        abort(404)
    task = get_task_info(task_id)
    form = SubmitTaskForm()
    if form.validate_on_submit():
        program = form.code.data.read().decode('utf-8').replace('\r', '')
        language = form.language.data
        submission = Submission(
            program=program,
            language=language,
            user_id=current_user.id,
            task_id=task['id']
        )
        db.session.add(submission)
        db.session.commit()
        submission.launch_task(
            'judge_py' if language == 'py' else 'judge_cpp',
            'Judging...',
            submission.id,
            get_task_files(task['id'], 'inputs'), program, get_task_files(task['id'], 'outputs'),
            task['python_tle'] if language == 'py' else task['cpp_tle']
        )
        db.session.commit()
        return redirect(url_for('submis.submission', submission_id=submission.id))
    return render_template('submit_task.html', task=task, form=form)
