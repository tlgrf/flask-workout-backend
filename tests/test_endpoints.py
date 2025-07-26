import json
import pytest

def test_exercise_crud(client):
    # CREATE
    r = client.post('/exercises', json={
        "name": "Push Up",
        "category": "strength",
        "equipment_needed": False
    })
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Push Up"
    eid = data["id"]

    # GET list
    r = client.get('/exercises')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list) and len(r.get_json()) == 1

    # GET single
    r = client.get(f'/exercises/{eid}')
    assert r.status_code == 200
    assert r.get_json()["category"] == "strength"

    # DELETE
    r = client.delete(f'/exercises/{eid}')
    assert r.status_code == 204
    # now 404
    r = client.get(f'/exercises/{eid}')
    assert r.status_code == 404

def test_workout_crud_and_link(client):
    # initially empty
    r = client.get('/workouts')
    assert r.status_code == 200 and r.get_json() == []

    # CREATE workout
    r = client.post('/workouts', json={"duration_minutes": 45})
    assert r.status_code == 201
    wo = r.get_json()
    assert wo["duration_minutes"] == 45
    wid = wo["id"]

    # GET single
    r = client.get(f'/workouts/{wid}')
    assert r.status_code == 200

    # CREATE exercise
    r = client.post('/exercises', json={
        "name": "Plank",
        "category": "strength",
        "equipment_needed": False
    })
    assert r.status_code == 201
    eid = r.get_json()["id"]

    # LINK exercise → workout
    r = client.post(f'/workouts/{wid}/exercises/{eid}/workout_exercises',
                    json={"duration_seconds": 60})
    assert r.status_code == 201
    we = r.get_json()
    assert we["duration_seconds"] == 60

    # bad payload → 400
    r = client.post(f'/workouts/{wid}/exercises/{eid}/workout_exercises',
                    json={})
    assert r.status_code == 400

    # DELETE workout
    r = client.delete(f'/workouts/{wid}')
    assert r.status_code == 204
    r = client.get(f'/workouts/{wid}')
    assert r.status_code == 404