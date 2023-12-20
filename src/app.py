"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Create User

@app.route('/user', methods=['POST'])
def handle_add_user():
    user = User()
    jason_data = request.get_json() 
    user.email = jason_data["email"]
    user.username = jason_data["username"]
    user.password = jason_data["password"]

    db.session.add(user)
    db.session.commit()

    return "user created", 201

#Get a list of all the people in the database

@app.route('/user', methods=['GET'])
def handle_get_users():
   all_users = User.query.all()
   all_users = list(map(lambda item: item.serialize(), all_users))
   results = all_users

   if not results:
       return jsonify({"msg": "There are no users "}), 404

   response_body = {
       "results": results
   }

   return jsonify(response_body), 200

#Get a one single people information

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_get_one_user(user_id):
    one_user = User.query.filter_by(id=user_id).first()

    if one_user is None:
         return jsonify({"msg": "User dont exist"}), 404

    response_body = {
        "nombre_usuario": one_user.serialize()
    }

    return jsonify(response_body), 200

#Create Planet

@app.route('/planet', methods=['POST'])
def handle_add_planet():
    planet = Planet()
    jason_data = request.get_json() 
    planet.name = jason_data["name"]
    planet.diameter = jason_data["diameter"]
    planet.rotation_period = jason_data["rotation_period"]
    planet.orbital_period = jason_data["orbital_period"]
    planet.gravity = jason_data["gravity"]
    planet.population = jason_data["population"]
    planet.climate = jason_data["climate"]
    planet.terrain = jason_data["terrain"]
    planet.surface_water = jason_data["surface_water"]

    db.session.add(planet)
    db.session.commit()

    return "user created", 201



#Get a list of all the planets in the database

@app.route('/planet', methods=['GET'])
def handle_get_all_planets():

    all_planets = Planet.query.all()
    all_planets = list(map(lambda item: item.serialize(),all_planets))
    results = all_planets

    if results == []:
         return jsonify({"msg":"No hay planetas "}), 404

    response_body = {
        "results": results
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
