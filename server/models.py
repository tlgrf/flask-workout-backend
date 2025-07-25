from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import date

db = SQLAlchemy()

class Exercise(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(80), nullable=False, unique=True)
    category         = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, value):
        assert len(value) >= 3, "Name must be ≥3 chars"
        return value

    @validates('category')
    def validate_category(self, key, value):
        assert value in ('strength','cardio','flexibility','balance'), "Invalid category"
        return value


class Workout(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    date             = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes            = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        assert value > 0, "Duration must be positive"
        return value


class WorkoutExercise(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    workout_id       = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id      = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    reps             = db.Column(db.Integer)
    sets             = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Table constraints: at least one of reps/sets or duration must be present
    __table_args__ = (
        db.CheckConstraint('(reps IS NOT NULL AND sets IS NOT NULL) OR duration_seconds IS NOT NULL', 
                           name='ck_reps_sets_or_duration'),
    )