from flask import render_template, Blueprint, abort
from flask_login import login_required, current_user
from app.models import Submission
from app.submit.utils import get_result, get_result_color, verdict_to_word, get_verdicts_colors
from app.lang import lang_to_string
from app.utils.colors_enum import Color
from app.utils.get_task import get_task_info
from rq import get_current_job
import sys

submis = Blueprint('submis', __name__)

@submis.route('/submission/view/<submission_id>')
@login_required
def submission(submission_id):
    submission = Submission.query.get(submission_id)
    if not submission:
        abort(404)

    task = get_task_info(submission.task_id)
    language = lang_to_string[submission.language]
    if submission.get_tasks_in_progress():
        return render_template(
            'submission_judging.html',
            submission=submission,
            progress=submission.get_task_in_progress().get_progress(),
            task=task,
            language=language,
            purple_color=Color.JUDGING.value
        )

    result = get_result(submission.status)
    result_color = get_result_color(submission.status)
    verdicts = verdict_to_word(submission.status)
    verdict_colors = get_verdicts_colors(submission.status)
    return render_template(
        'submission.html',
        submission=submission,
        task=task,
        result=result,
        language=language,
        result_color=result_color,
        verdicts=verdicts,
        verdict_colors=verdict_colors
    )


@submis.route('/submissions/<task_id>')
@login_required
def submissions(task_id):
    task = get_task_info(task_id)
    submissions = Submission.query.filter_by(
        task_id=task_id, user_id=current_user.id).order_by(Submission.date_submitted.desc())
    languages = [lang_to_string[submission.language]
                 for submission in submissions]
    code_times = ["" if not submission.times else str(
        max(submission.times)) + " ms" for submission in submissions]
    verdicts = []
    for submission in submissions:
        if not submission.status:
            verdicts.append(2)
        else:
            verdicts.append(
                all(status == 'AC' for status in submission.status))
    verdicts_colors = []
    for verdict in verdicts:
        if verdict == 2:
            verdicts_colors.append(Color.JUDGING.value)
        elif verdict:
            verdicts_colors.append(Color.ACCEPTED.value)
        else:
            verdicts_colors.append(Color.WRONG_ANSWER.value)
    return render_template('submissions.html',
                           submissions=submissions,
                           task=task,
                           languages=languages,
                           code_times=code_times,
                           verdicts=verdicts,
                           verdicts_colors=verdicts_colors
                           )
