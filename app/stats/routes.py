from flask import render_template, Blueprint
from app.models import Submission, User

stats = Blueprint('stats', __name__)

@stats.route('/leaderboard')
def leaderboard():
    table = []
    people = {}
    submissions = Submission.query.all()

    for submission in submissions:
        user_id = submission.user_id
        task_id = submission.task_id
        if submission.status and all(result == 'AC' for result in submission.status):
            if user_id not in people:
                people[user_id] = set()
            people[user_id].add(task_id)

    for user_id in people:
        username = User.query.get(user_id).username
        table.append([len(people[user_id]), username])

    table.sort(reverse=True)
    for i in range(len(table)):
        table[i] = [i + 1, table[i][1], table[i][0]]

    return render_template('leaderboard.html', table=table)