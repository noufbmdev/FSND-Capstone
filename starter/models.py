from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


# setup_db(app) binds a flask application and a SQLAlchemy service
def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()


class Movie (db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    releaseDate = db.Column(db.DateTime)
    actors = db.relationship('Actor', secondary='movies_actors')

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def add(self):
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
            'releaseDate': self.releaseDate,
            'actors': self.actors
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor (db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    movies = db.relationship('Movie', secondary='movies_actors')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def add(self):
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

    def __repr__(self):
        return json.dumps(self.format())


class MoviesActors(db.Model):
    __tablename__ = 'movies_actors'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column('movie_id',
                         db.Integer,
                         db.ForeignKey('movie.id'),
                         primary_key=True)
    actor_id = db.Column('actor_id',
                         db.Integer,
                         db.ForeignKey('actor.id'),
                         primary_key=True)
