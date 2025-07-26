from flask import Flask, request, jsonify, make_response, abort
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import exercise_schema, exercises_schema, workout_schema, workouts_schema, we_schema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.errorhandler(ValidationError)
def handle_marshmallow(err):
    return {'errors': err.messages}, 400

db.init_app(app)
migrate = Migrate(app, db)

# ---------- ROUTES BELOW ----------
@app.route('/exercises', methods=['GET'])
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    ex = db.session.get(Exercise, id) or abort(404)
    return jsonify(exercise_schema.dump(ex)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = exercise_schema.load(request.json)
    ex = Exercise(**data)
    db.session.add(ex); db.session.commit()
    return jsonify(exercise_schema.dump(ex)), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    ex = Exercise.query.get_or_404(id)
    db.session.delete(ex); db.session.commit()
    return '', 204

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    wo = Workout.query.get_or_404(id)
    return jsonify(workout_schema.dump(wo)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = workout_schema.load(request.json)
    wo = Workout(**data)
    db.session.add(wo); db.session.commit()
    return jsonify(workout_schema.dump(wo)), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    wo = Workout.query.get_or_404(id)
    db.session.delete(wo); db.session.commit()
    return '', 204

@app.route('/workouts/<int:wid>/exercises/<int:eid>/workout_exercises', methods=['POST'])
def add_ex_to_workout(wid, eid):
    we_data = we_schema.load(request.json)
    we = WorkoutExercise(workout_id=wid, exercise_id=eid, **we_data)
    db.session.add(we); db.session.commit()
    return jsonify(we_schema.dump(we)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)