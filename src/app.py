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
from models import Character, Planet, db, User
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

#Get a list of all users in the database

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

#Get a one single user information

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_get_one_user(user_id):
    one_user = User.query.filter_by(id=user_id).first()

    if one_user is None:
         return jsonify({"msg": "User dont exist"}), 404

    response_body = {
        "user_name": one_user.serialize()
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

    return "planet created", 201


#Get a list of all the planets in the database

@app.route('/planets', methods=['GET'])
def handle_get_all_planets():

    all_planets = Planet.query.all()
    all_planets = list(map(lambda item: item.serialize(),all_planets))
    results = all_planets

    if results == []:
         return jsonify({"msg":"There is no planets "}), 404

    response_body = {
        "results": results
    }

    return jsonify(response_body), 200

#Get one planet

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet(planet_id):

    print(planet_id)
    planet_query = Planet.query.filter_by(id= planet_id).first()
    print(planet_query)

    if planet_query is None:
         return jsonify({"msg":"Planet dont exist"}), 404


    response_body = {
        "msg": "This is the planet requested",
        "result": planet_query.serialize()
    }

    return jsonify(response_body), 200

#Create a character

@app.route('/people', methods=['POST'])
def handle_add_people():
   people = Character()
   jason_data = request.get_json()
   people.Name = jason_data ["Name"]
   people.Height = jason_data ["Height"]
   people.Mass = jason_data ["Mass"],
   people.Hair_Color = jason_data ["Hair_Color"],
   people.Skin_Color = jason_data ["Skin_Color"],
   people.Eye_Color = jason_data ["Eye_Color"],
   people.Birth_Year =jason_data ["Birth_Year"],
   people.Gender = jason_data ["Gender"]
  
   db.session.add(people)
   db.session.commit()

   return "Person created", 201

#Get a list of all the people in the database

@app.route('/people', methods=['GET'])
def get_people():

    people_query = Character.query.all()

    results = list(map(lambda item: item.serialize(),people_query))
    print(results)

    if results == []:
         return jsonify({"msg":"Character dont exist"}), 404


    response_body = {
        "msg": "This are the characters",
        "results": results
    }

    return jsonify(response_body), 200

#Get a one single people information

@app.route('/people/<int:people_id>', methods=['GET'])
def people(people_id):

    print(people_id)
    people_query = Character.query.filter_by(id= people_id).first()
    print(people_query)

    if people_query is None:
         return jsonify({"msg":"Character dont exist"}), 404


    response_body = {
        "msg": "People ",
        "result": people_query.serialize()
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
