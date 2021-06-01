from flask import render_template, Blueprint

learn = Blueprint('learn', __name__)

@learn.route('/learn/topics')
def topics():
    return render_template('topics.html')

@learn.route('/learn/heap')
def heap():
    return render_template('learn/heap.html')

@learn.route('/learn/dijkstra')
def dijkstra():
    return render_template('learn/dijkstra.html')

@learn.route('/learn/unionfind')
def unionfind():
    return render_template('learn/unionfind.html')

@learn.route('/learn/articulations')
def articulations():
    return render_template('learn/articulations.html')