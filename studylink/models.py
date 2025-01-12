#!/usr/bin/python3
"""
This module defines the database models for the StudyLink application.
"""

from datetime import datetime
from studylink import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  """
  Function to load a user given their ID using Flask-Login's user_loader callback.
  """
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  """
  User model representing a user of the application.
  """
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(60), nullable=False, default='profile.jpg')
  password = db.Column(db.String(60), nullable=False)
  joined = db.Column(db.DateTime, default=datetime.utcnow)
  website = db.Column(db.String(120))
  twitter = db.Column(db.String(100))
  github = db.Column(db.String(100))
  confirmed = db.Column(db.Boolean, default=False)
  confirmed_on = db.Column(db.DateTime, nullable=True)
  user_fields = db.relationship('UserFields', backref='user', lazy=True, cascade='all, delete-orphan')
  user_resources = db.relationship('UserResources', backref='user', lazy=True, cascade='all, delete-orphan')
  reviews = db.relationship('Reviews', backref='user', lazy=True, cascade='all, delete-orphan')
  replies = db.relationship('Reply', backref='user', lazy=True, cascade='all, delete-orphan')
  resources = db.relationship('Resources', back_populates='user', cascade='all, delete-orphan')

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Fields(db.Model):
  """
  Fields model representing fields of study.
  """
  __tablename__ = 'fields'
  id = db.Column(db.Integer, primary_key=True)
  field_name = db.Column(db.String(60), nullable=False)
  courses = db.relationship('Courses', backref='fields', lazy=True)

  def __repr__(self):
    return f"Fields('{self.field_name}')"


class Courses(db.Model):
  """
  Courses model representing courses within a field of study.
  """
  __tablename__ = 'courses'
  id = db.Column(db.Integer, primary_key=True)
  course_name = db.Column(db.String(60), nullable=False)
  field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)

  def __repr__(self):
    return f"Fields('{self.course_name}')"


class UserFields(db.Model):
  """
  UserFields model representing user selections of fields and courses.
  """
  __tablename__ = 'userFields'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
  course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

  fields = db.relationship('Fields', backref=db.backref('user_fields', lazy=True))
  courses = db.relationship('Courses', backref=db.backref('user_fields', lazy=True))

  def __repr__(self):
    return f"User Fields('{self.user_id}', '{self.course_id}')"


class Resources(db.Model):
  """
  Resources model representing shared resources.
  """
  __tablename__ = 'resources'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', back_populates='resources')
  title = db.Column(db.String(120), nullable=False)
  url = db.Column(db.Text, nullable=False)
  description = db.Column(db.Text, nullable=False)
  thumbnail = db.Column(db.String(60), nullable=False, default="profile.jpg")
  course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  reviews = db.relationship('Reviews', backref='resource', lazy=True)

  def __repr__(self):
    return f"Post('{self.title}', '{self.description}', '{self.url}', '{self.date_posted}')"


class UserResources(db.Model):
  """
  UserResources model representing user-saved resources.
  """
  __tablename__ = 'userResources'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)

  def __repr__(self):
    return f"Interest('{self.user_id}', '{self.resource}')"


class Reviews(db.Model):
  """
  Reviews model representing reviews on resources.
  """
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'))
  review = db.Column(db.Text, nullable=False)
  review_date = db.Column(db.DateTime, default=datetime.utcnow)
  replies = db.relationship('Reply', backref='reviews', lazy=True)


class Reply(db.Model):
  """
  Reply model representing replies to reviews.
  """
  __tablename__ = 'reply'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))
  reply = db.Column(db.Text)
  reply_date = db.Column(db.DateTime, default=datetime.utcnow)
