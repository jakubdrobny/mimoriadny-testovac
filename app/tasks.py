import time, sys
from rq import get_current_job
from app import create_app, db
from app.models import Task, Submission
from flask import has_app_context
from subprocess import Popen, PIPE, run
import os

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        if progress >= 100:
            task.complete = True
        db.session.commit()

def judge_py(submission_id, input_files, program, output_files, timeout=5):
    _set_task_progress(0)
    submission = Submission.query.get(submission_id)
    outputs = []
    verdicts = []
    times = []
    old_path = os.getcwd()
    os.chdir(old_path + '/isolate')
    for i in range(len(input_files)):
        try:
            _set_task_progress(100 * i // len(input_files))
            child_process = Popen(['isolate', '--init'], stdin=PIPE, stdout=PIPE)
            isolate_path, _ = child_process.communicate()
            isolate_path = isolate_path.decode()
            isolate_path = isolate_path[:-1]
            with open(isolate_path + "/box/0.in", 'w+') as f:
                f.write(input_files[i])
            with open(isolate_path + '/box/0.out', 'w') as f:
                pass
            child_process = Popen(
                [
                    'isolate',
                    '--time=%d'%(timeout),
                    '--stdin=0.in',
                    '--stdout=0.out',
                    '--run', '--',
                    '/usr/bin/pypy3', '-c', program
                ],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, errors = child_process.communicate()
            errors = errors.decode()
            if 'Time limit exceeded' in errors:
                outputs.append('')
                times.append(timeout * 1000)
                verdicts.append('TLE')
                run(["isolate", "--cleanup"])
                continue
            if errors[:2] != 'OK':
                outputs.append('')
                verdicts.append('RE')
                times.append(69420)
                run(["isolate", "--cleanup"])
                continue
            execution_time = int(1000 * float(errors.split()[1][1:]))
            child_process = Popen(['cat', isolate_path + '/box/0.out'], stdout=PIPE)
            output, _ = child_process.communicate()
            output = output.decode()
            if errors[:2] == 'OK':
                outputs.append(output)
                times.append(execution_time)
                verdicts.append('AC' if output == output_files[i] else 'WA')
            run(["isolate", "--cleanup"])
        except:
            outputs.append('')
            verdicts.append('RE')
            times.append(69420)
            run(["isolate", "--cleanup"])
    os.chdir(old_path)
    submission.status = verdicts
    submission.times = times
    db.session.commit()
    _set_task_progress(100)

def judge_cpp(submission_id, input_files, program, output_files, timeout=1):
    _set_task_progress(0)
    submission = Submission.query.get(submission_id)
    outputs = []
    verdicts = []
    times = []
    old_path = os.getcwd()
    os.chdir(old_path + '/isolate')
    for i in range(len(input_files)):
        run(["isolate", "--cleanup"])
        try:
            _set_task_progress(100 * i // len(input_files))
            child_process = Popen(['isolate', '--init'], stdin=PIPE, stdout=PIPE)
            isolate_path, _ = child_process.communicate()
            isolate_path = isolate_path.decode()
            isolate_path = isolate_path[:-1]
            with open(isolate_path + "/box/a.cpp", 'w+') as f:
                f.write(program)
            with open(isolate_path + "/box/0.in", 'w+') as f:
                f.write(input_files[i])
            child_process = Popen(
                [
                    'isolate',
                    '-p',
                    '--run', '--',
                    '/usr/bin/g++', '-B/usr/bin',
                    'a.cpp',
                    '--std=c++17',
                    '-O2',
                    '-o',
                    'a'
                ],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, errors = child_process.communicate()
            errors = errors.decode()
            if errors[:2] != 'OK':
                outputs.append('')
                verdicts.append('RE')
                times.append(69420)
                run(["isolate", "--cleanup"])
                continue
            child_process = Popen(
                [
                    'isolate',
                    '--time=%d'%(timeout),
                    '--stdin=0.in',
                    '--run', '--',
                    './a'
                ],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, errors = child_process.communicate()
            output = output.decode()
            errors = errors.decode()
            if 'Time limit exceeded' in errors:
                outputs.append('')
                times.append(timeout * 1000)
                verdicts.append('TLE')
                run(["isolate", "--cleanup"])
                continue
            execution_time = int(1000 * float(errors.split()[1][1:]))
            if errors[:2] == 'OK':
                outputs.append(output)
                times.append(execution_time)
                verdicts.append('AC' if output == output_files[i] else 'WA')
                # print(output, output_files[i], file=sys.stderr)
            run(["isolate", "--cleanup"])
        except:
            outputs.append('')
            verdicts.append('RE')
            times.append(69420)
            run(["isolate", "--cleanup"])
    os.chdir(old_path)
    submission.status = verdicts
    submission.times = times
    db.session.commit()
    _set_task_progress(100)