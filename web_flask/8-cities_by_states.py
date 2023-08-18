#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template
from models.city import City
from models.state import State
import models


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def list_states():
    """ Function that returns a template """
    cities_of_states = models.storage.all(State)
    all_states = []
    for k, v in cities_of_states.items():
        all_states.append(v)
    return render_template('8-cities_by_states.html', all_states=all_states)


@app.teardown_appcontext
def tear_down(self):
    """ tear down """
    models.storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
