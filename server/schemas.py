from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class ExerciseSchema(Schema):
    id               = fields.Int(dump_only=True)
    name             = fields.Str(required=True, validate=validate.Length(min=3))
    category         = fields.Str(required=True,
                           validate=validate.OneOf(['strength','cardio','flexibility','balance']))
    equipment_needed = fields.Bool(required=True)
    workout_exercises = fields.Nested("WorkoutExerciseSchema", many=True, data_key="workouts")

class WorkoutSchema(Schema):
    id               = fields.Int(dump_only=True)
    date             = fields.Date()
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes            = fields.Str()
    workout_exercises = fields.Nested("WorkoutExerciseSchema", many=True, data_key="exercises")

class WESchema(Schema):
    reps             = fields.Int(validate=validate.Range(min=1))
    sets             = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int(validate=validate.Range(min=1))

    @validates_schema
    def check_one(self, data, **kwargs):
        if not ((data.get('reps') and data.get('sets')) or data.get('duration_seconds')):
            raise ValidationError('Must include reps+sets or duration_seconds')

class WorkoutExerciseSchema(Schema):
    exercise = fields.Nested(ExerciseSchema, only=("id","name","category"))
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

exercise_schema  = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema   = WorkoutSchema()
workouts_schema  = WorkoutSchema(many=True)
we_schema        = WESchema()