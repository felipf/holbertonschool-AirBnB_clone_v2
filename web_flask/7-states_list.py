#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask
from flask import render_template
import models
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Function that returns a template """
    states = models.storage.all(State)
    all_states = []
    for k, v in states.items():
        all_states.append(v)
    return render_template('7-states_list.html', all_states=all_states)


@app.teardown_appcontext
def teardown_db(exception):
    """ Function that removes the current SQLAlchemy Session """
    models.storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
