# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response ,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake_info= Earthquake.query.get(id)
    if not earthquake_info:
        return jsonify({'message': f'Earthquake {id} does not exist.'}), 404
    else:
        return jsonify({
            'id': earthquake_info.id,
            'location': earthquake_info.location,
            'magnitude': earthquake_info.magnitude,
            'year': earthquake_info.year
        }), 
   
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_magnitude(magnitude):
    earthquakes_magnitude_info = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if not earthquakes_magnitude_info:
        return jsonify({
            'count': 0,
            'quakes': []
        }), 200
    else:
        earthquakes_info = [{
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        } for earthquake in earthquakes_magnitude_info]
        return jsonify({
            'count': len(earthquakes_info),
            'quakes': earthquakes_info
        }), 200
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)
