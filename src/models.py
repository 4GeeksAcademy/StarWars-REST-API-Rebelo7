from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_Active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.String(80), unique=False, nullable=False)
    rotation_period = db.Column(db.String(80), unique=False, nullable=False)
    orbital_period = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }   
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120), unique=True, nullable=False)
    Height = db.Column(db.String(80), unique=False, nullable=False)
    Mass = db.Column(db.String(80), unique=False, nullable=False)
    Hair_Color = db.Column(db.String(80), unique=False, nullable=False)
    Skin_Color = db.Column(db.String(80), unique=False, nullable=False)
    Eye_Color = db.Column(db.String(80), unique=False, nullable=False)
    Birth_Year = db.Column(db.String(80), unique=False, nullable=False)
    Gender = db.Column(db.String(80), unique=False, nullable=False)
    
    
    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "Name": self.Name,
            "Height": self.Height,
            "Mass": self.Mass,
            "Hair_Color": self.Hair_Color,
            "Skin_Color": self.Skin_Color,
            "Eye_Color": self.Eye_Color,
            "Birth_Year": self.Birth_Year,
            "Gender": self.Gender,
        }
    
class Favorite(db.Model):
   __tablename__ = "favorite"
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
   user = db.relationship("User")
   character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
   character = db.relationship("Character")
   planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
   planet = db.relationship("Planet")
   
   __table_args__ = (
       db.UniqueConstraint(
           "user_id",
           "character_id",
           "planet_id",
           name="uq_user_favorites",
       ),
   )

   def __repr__(self):
       return "{}".format(self.user_id.user_name)

   def serialize(self):
       data = {
           "user_id": self.user_id,
           "user_name": self.user_id.user_name if self.user_id else None,
           "type": "Favorite",
       }
       if self.character_id:
           data["object_id"] = self.character_id
       elif self.planet_id:
           data["object_id"] = self.planet_id
       return data