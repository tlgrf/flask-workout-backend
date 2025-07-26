import pytest
from server.models import Exercise, Workout
from server.models import db

def test_exercise_name_too_short(app):
    with app.app_context():
        with pytest.raises(AssertionError):
            ex = Exercise(name='AB', category='strength', equipment_needed=True)
            db.session.add(ex); db.session.commit()

def test_exercise_invalid_category(app):
    with app.app_context():
        with pytest.raises(AssertionError):
            ex = Exercise(name='Squat', category='foo', equipment_needed=True)
            db.session.add(ex); db.session.commit()

def test_workout_negative_duration(app):
    with app.app_context():
        with pytest.raises(AssertionError):
            wo = Workout(duration_minutes=0)
            db.session.add(wo); db.session.commit()