# server/app.py
#!/usr/bin/env python3
#import jsonify from flask
from flask import Flask, make_response,jsonify
from flask_migrate import Migrate
#import Earthquake model
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
# Add a new route to handle requests to `/earthquakes/<int:id>`.
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquakes(id):
    earthquake = db.session.get(Earthquake,id)
    if earthquake:
        return jsonify({
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }),200
    else:
        return jsonify({
            'message':f'Earthquake {id} not found.'
        }),404
# Add view to get earthquakes that match a minimum magnitude value
@app.route('/earthquakes/magnitude/<float:magnitude>',methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    #Query the database and format responses
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]
    return jsonify({
        'count': len(quake_list),
        'quakes': quake_list
    }), 200
if __name__ == '__main__':
    app.run(port=5555, debug=True)
