from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,unique=True, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    user_password = db.Column(db.String(80), nullable=False)
    user_favourite_character = db.relationship("Favourite_characters", backref="user")
    user_favourite_planet = db.relationship("Favourite_planets", backref="user")
    

    def __repr__(self):
        return '<User %r>' % self.user_email

    def serialize(self):
        return {
            "id": self.user_id,
            "email":self.user_email,
            "favourite_characters": [favourite.serialize() for favourite in self.user_favourite_character],
            "favourite_planets": [favourite.serialize() for favourite in self.user_favourite_planet]
            
        }


class Characters(db.Model):
    __tablename__ = "characters"
    character_id = db.Column(db.Integer ,unique=True,primary_key=True )
    character_name = db.Column(db.String(100), nullable=False )
    character_race = db.Column(db.String(100),nullable=False)
    character_age = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Characters %r>' % self.character_name

    def serialize(self):
        return {
            "id": self.character_id,
            "name": self.character_name,
            "race": self.character_race,
            "age": self.character_age
        }
           

class Planets(db.Model):
    __tablename__ = "planets"
    planet_id = db.Column(db.Integer,unique=True, primary_key=True )    
    planet_name = db.Column(db.String(100), nullable=False )
    planet_size = db.Column(db.String(100), nullable=False)
    planet_age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.planet_id

    def serialize(self):
        return {
            "id": self.planet_id,
            "name": self.planet_name,
            "size": self.planet_size,
            "age": self.planet_age
        }


class Favourite_characters(db.Model):
    __tablename__ = "favourite_characters"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.character_id")) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id")) 
    character = db.relationship("Characters")
    

    def __repr__(self):
        return '<Favourite_characters %r>' % self.user_id

    def serialize(self):
        return {
            "user": self.user_id,
            "character": self.character_id,
            
        }

class Favourite_planets(db.Model):
    __tablename__ = "favourite_planets"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    planet_id= db.Column(db.Integer, db.ForeignKey("planets.planet_id"))
    user_id= db.Column(db.Integer, db.ForeignKey("user.user_id")) 
    planet = db.relationship("Planets")
    




    def __repr__(self):
        return '<Favourite_planets %r>' % self.user_id

    def serialize(self):
        return {
            "user": self.user_id,
            "planet": self.planet_id,
        }