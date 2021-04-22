import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

# ---------------------------------------------------------------------------------------------------#
# App Configurations
# ---------------------------------------------------------------------------------------------------#
# database_path = "postgresql://postgres:root@localhost:5432/trivia"

database_path = os.environ.get('DATABASE_URL')
# database_path = "postgresql://postgres:root@localhost:5432/capstone"
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/capstoneexp"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def drop_all_and_create_all():
  db.drop_all()
  db.create_all()

  # Dummy Entries for Actor
  lenonardo = Actor('Leonardo',55,"Male")
  salman = Actor('Salman',50,"Male")
  vivek = Actor('Vivek',22,"Male")
  pranshant = Actor('Pranshant',50,"Male")
  katrina = Actor('Katrina',50,"Female")
  naina = Actor('Naina',50,"Male")
  shahrukh = Actor("Shahrukh", 44, "Male")

  # Dummy Data for Movies
  movie1 = Movie("Black Diamond", 2011, 1)
  movie2 = Movie("King Kong", 2010, 1)
  movie3 = Movie("Tarzan", 2008, 2)
  movie4 = Movie("Harry Potter", 2012, 3)
  movie5 = Movie("Narnia", 2020, 4)
  movie6 = Movie("Zootopia", 1700, 5)
  movie7 = Movie("lalaland", 2001, 6)
  movie8 = Movie("Lion King", 2001, 7)


  # Dummy data insertion into Actor Model
  lenonardo.insert()
  salman.insert()
  vivek.insert()
  pranshant.insert()
  shahrukh.insert()
  katrina.insert()
  naina.insert()

  # Dummy data insertion into Movie Model
  movie1.insert()
  movie2.insert()
  movie3.insert()
  movie4.insert()
  movie5.insert()
  movie6.insert()
  movie7.insert()
  movie8.insert()

'''
Actor Model

'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  movie = db.relationship('Movie', backref=db.backref('actor'), cascade="delete", lazy=True)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
    }

'''
Movie Model

'''
class Movie(db.Model):
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_year = Column(Integer)
  actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)

  def __init__(self, title, release_year, actor_id):
    self.title = title
    self.release_year = release_year
    self.actor_id = actor_id

  def get_title(self):
    return self.title

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_year': self.release_year,
      'actor_id': self.actor_id,
    }