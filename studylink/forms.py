#!/usr/bin/python3
""" This module defines various FlaskForm classes for the StudyLink application """

import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from studylink.models import User

def validate_password_strength(form, field):
    """ Validate the strength of the password """
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    if not re.search(r"[a-z]", password):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r"[A-Z]", password):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search(r"[0-9]", password):
        raise ValidationError('Password must contain at least one digit')

class RegistrationForm(FlaskForm):
  """ Form for user registration """
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), validate_password_strength])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    """ Validate that the username is not already taken """
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken, please choose a different username')

  def validate_email(self, email):
    """ Validate that the email is not already taken """
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken, please choose a different email')


class LoginForm(FlaskForm):
  """ Form for user login """
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
  """ Form for updating user account information """
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  website = StringField('Website')
  twitter = StringField('Twitter')
  github = StringField('Github')
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Update')

  def validate_username(self, username):
    """ Validate that the new username is not already taken """
    if username.data != current_user.username:  
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('That username is taken, please choose a different username')
   
  def validate_email(self, email):
    """ Validate that the new email is not already taken """
    if email.data != current_user.email: 
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('That email is taken, please choose a different email')


class AddResourceForm(FlaskForm):
  """ Form for adding a new resource """
  link = StringField("Link to Resource", validators=[DataRequired()])
  comment = TextAreaField("Description", validators=[DataRequired()])
  submit = SubmitField("Get Resource")

