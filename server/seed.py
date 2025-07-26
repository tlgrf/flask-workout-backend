#!/usr/bin/env python3
from server.app import app, db
from server.models import Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    ex1 = Exercise(name='Bench Press', category='strength', equipment_needed=True)
    ex2 = Exercise(name='Running', category='cardio', equipment_needed=False)
    wo1 = Workout(date=date(2025,7,25), duration_minutes=60, notes='Leg day')
    we1 = WorkoutExercise(workout=wo1, exercise=ex1, reps=10, sets=3)

    db.session.add_all([ex1, ex2, wo1, we1])
    db.session.commit()
    print("🌱 Seeded data!")