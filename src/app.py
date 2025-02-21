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
from models import db, User, Favourite_characters, Favourite_planets, Characters, Planets
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

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    character_info = [characters.serialize() for characters in characters]
    return jsonify(character_info), 200


@app.route('/characters/<int:id>', methods=['GET'])
def get_characters_by_id(id):
    characters = Characters.query.get(id)
    character_info = characters.serialize() 
    return jsonify(character_info), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planet_info = [planets.serialize() for planets in planets]
    return jsonify(planet_info), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planets_by_id(id):
    planets = Planets.query.get(id)
    planet_info = planets.serialize() 
    return jsonify(planet_info), 200


@app.route('/users', methods=['GET'])
def get_people():
    users = User.query.all()
    user_info = [users.serialize() for users in users]
    return jsonify(user_info), 200


@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def user_favorites(user_id):
    user = User.query.get(user_id)
    user_info = user.serialize()
    favourite_character = user_info["favourite_characters"]
    favourite_planet = user_info["favourite_planets"]
    return jsonify(favourite_character, favourite_planet), 200

@app.route('/users/<int:user_id>/favorites/<int:planet_id>', methods=['POST'])
def new_favorite_planet(user_id, planet_id):
    liked = Favourite_planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if liked:
        return jsonify({"msg": "Already a favourite"})
    new_like = Favourite_planets(user_id=user_id,planet_id=planet_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"msg":"Added new favourite planet"}), 200

@app.route('/users/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def new_favorite_character(user_id, character_id):
    liked = Favourite_characters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if liked:
        return jsonify({"msg": "Already a favourite"})
    new_like = Favourite_characters(user_id=user_id,character_id=character_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"msg":"Added new favourite character"}), 200

@app.route('/users/<int:user_id>/favourite/planet/<int:planet_id>', methods=["DELETE"])
def delete_planet_favourite(user_id, planet_id):
    like = Favourite_planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({"msg":"Planet deleted from favourites"})
    return jsonify({"msg":"The planet was not found in the user favourites"})

@app.route('/users/<int:user_id>/favourite/character/<int:character_id>', methods=["DELETE"])
def delete_character_favourite(user_id, character_id):
    like = Favourite_characters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({"msg":"Planet deleted from favourites"})
    return jsonify({"msg":"The planet was not found in the user favourites"})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
