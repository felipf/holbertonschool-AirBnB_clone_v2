#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template
import models
from models.state import State
from models.city import City
from models.amenity import Amenity


app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    """ tear down """
    models.storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def show_page():
    """ display html page """
    cities_of_states = models.storage.all(State)
    grp_amenitis = models.storage.all(Amenity)
    all_states = []
    all_amenities = []

    for k, v in cities_of_states.items():
        all_states.append(v)
    for k, v in grp_amenitis.items():
        all_amenities.append(v)
    return render_template('10-hbnb_filters.html', all_states=all_states,
                           all_amenities=all_amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
