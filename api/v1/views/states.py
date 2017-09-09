#!/usr/bin/python3
"""Use REST structure with states in database"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage, CNC
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Show all states in json format with GET request"""
    try:
        states = []
        for state in storage.all('State').values():
            states.append(state.to_json())
        return (jsonify(states))
    except:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_new_state():
    """Create new state with POST request"""
    kwargs = request.get_json()

    if kwargs is None:
        return ('Not a JSON', 400)
    if kwargs.get('name') is None:
            abort('Missing name', 400)
    if 'name' not in kwargs:
        return ('Missing name', 400)

    # grab state class
    State = CNC.get('State')

    # create new_state object with name given POST
    new_state = State(**kwargs)

    new_state.save()
    return (jsonify(new_state.to_json()), 201)


# ###### requests with state id ################### #
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve state matching id"""
    state = storage.get('State', state_id)
    try:
        return (jsonify(state.to_json()))
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete state matching id with DELETE request"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_update_state(state_id):
    """Update an attribute in state object with PUT request"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    for k, v in kwargs.items():
        setattr(state, k, v)
    state.save()
    return (jsonify(state.to_json()), 200)
