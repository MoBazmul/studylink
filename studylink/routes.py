#!/usr/bin/python3
"""
This module defines the routes and views for the StudyLink application
"""

import os
import json
import secrets
from random import sample
from studylink import app, db, bcrypt
from studylink.models import User, Resources, Fields, Courses, UserFields, UserResources, Reviews, Reply
from studylink.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddResourceForm
from flask import jsonify, make_response, render_template, url_for, flash, redirect, request, session, current_app
from flask_login import login_user, current_user, logout_user, login_required
from studylink.get_youtube_videos import get_video_details

def initialize_database():
  """
  Initialize the database with predefined fields and courses if they do not exist.
  """
  with app.app_context():
    db.create_all()
    if Fields.query.count() == 0:
      with open('./software_fields_courses.json') as f:
        data = json.load(f)
        for field_data in data:
          for field_name, courses in field_data.items():
            field = Fields(field_name=field_name)
            db.session.add(field)
            db.session.flush()  # To get the field id
            for course_name in courses:
              course = Courses(course_name=course_name, field_id=field.id)
              db.session.add(course)
            db.session.commit()

initialize_database()


@app.route("/")
@app.route("/home")
def home():
  """
  Home page view. Displays resources based on the user's selected courses or all resources if not logged in.
  """
  resources_dict = {}

  if current_user.is_authenticated:
    # Assuming current_user is your user authentication object
    user_id = current_user.id
    user_fields = UserFields.query.filter_by(user_id=user_id).all()

    for user_field in user_fields:
      course_id = user_field.course_id
      course = Courses.query.get(course_id)
      resources = Resources.query.filter_by(course_id=course_id).all()
      if len(resources) >= 4:
        resources = sample(resources, 4)
      resources_dict[course.course_name] = resources
    
    return render_template("home.html", title="Home", resources_dict=resources_dict)

  # If not authenticated, show a sample of all resources
  resources = Resources.query.all()

  if len(resources) < 4:
      sampled_resources = resources
  else:
      sampled_resources = sample(resources, 4)
  
  return render_template("home.html", title="Home", resources=sampled_resources)



@app.route("/register", methods=['POST', 'GET'])
def register():
  """
  User registration view.
  """
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()

  if form.validate_on_submit():
    hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    
    # Log in the user immediately after registration
    login_user(user)
    
    flash(f'Your account has been created! You are now logged in.', 'success')
    return redirect(url_for('fields'))
  return render_template('registration.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  """
  User login view.
  """
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      
      # Set a cookie after successful login
      response = make_response(redirect(next_page or url_for('home')))
      response.set_cookie('user_id', str(user.id), max_age=30 * 24 * 60 * 60)  # Expires in 30 days
      return response
    else:
      flash('Login unsuccessful. Please check email and password.', 'danger')
  
  return render_template('login.html', title='Login', form=form)



@app.route('/fields')
@login_required
def fields():
  """
  View to display available fields of study.
  """
  fields = Fields.query.all()
  return render_template('fields.html', fields=fields)


@app.route('/courses', methods=['POST'])
@login_required
def courses():
  """
  View to display available courses based on the selected field.
  """
  selected_field_id = request.form.get('field')
  if not selected_field_id:
    return redirect(url_for('fields'))
    
  session['selected_field_id'] = selected_field_id
  selected_field = Fields.query.get(selected_field_id)
  courses = Courses.query.filter_by(field_id=selected_field_id).all()
  return render_template('courses.html', field=selected_field, courses=courses)


@app.route('/save_choices', methods=['POST'])
@login_required
def save_choices():
  """
  View to save the user's selected courses.
  """
  user_id = current_user.id 
  field_id = session.get('selected_field_id')
  selected_courses = request.form.getlist('courses')

  # Remove existing selections for the user and field
  user_field = UserFields.query.filter_by(user_id=user_id, field_id=field_id).delete()

  # Add new selections
  for course_id in selected_courses:
    user_field = UserFields(user_id=user_id, field_id=field_id, course_id=course_id)
    db.session.add(user_field)
    
  db.session.commit()
  return redirect(url_for('account'))


@app.route("/logout")
def logout():
  """
  User logout view.
  """
  logout_user()
  return redirect(url_for('home'))


def save_picture(form_picture):
    """
    Save the uploaded profile picture and return its filename.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    form_picture.save(picture_path)

    return picture_fn


@app.template_filter('format_datetime')
def format_datetime(value):
  """
  Custom filter to format datetime values in templates.
  """
  if value is None:
    return ""
  return value.strftime("%B %d, %Y")


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  """
  User account view to update profile information.
  """
  fields, courses = set(), set()
  
  user_id = current_user.id
  form = UpdateAccountForm()

  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.website = form.website.data
    current_user.twitter = form.twitter.data
    current_user.github = form.github.data
    db.session.commit()
    flash("Your account has been updated", 'success')
    return redirect(url_for('account'))
  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.website.data = current_user.website
    form.twitter.data = current_user.twitter
    form.github.data = current_user.github

  user_fields = UserFields.query.filter_by(user_id=user_id).all()

  for field in user_fields:
    fields.add(field.fields.field_name)

  for course in user_fields:
    courses.add(course.courses.course_name)
  
  fields_length = len(fields)
  courses_length = len(courses)

  image_file = url_for('static', filename='images/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form, courses=courses, fields=fields, fields_length=fields_length, courses_length=courses_length)


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
  """
  View to delete the user's account and all associated data.
  """
  user_id = current_user.id
  user = User.query.get(user_id)
  
  if user:
    # Delete all reviews associated with the user
    reviews = Reviews.query.filter_by(user_id=user_id).all()
    for review in reviews:
      db.session.delete(review)
    
    # Delete all resources associated with the user
    resources = Resources.query.filter_by(user_id=user_id).all()
    for resource in resources:
      db.session.delete(resource)
    
    # Delete all saved resources associated with the user
    saved_resources = UserResources.query.filter_by(user_id=user_id).all()
    for saved_resource in saved_resources:
      db.session.delete(saved_resource)
    
    # Commit the session to remove all associated records
    db.session.commit()

    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    logout_user()
    response = {"success": True, "message": "Account and all associated data deleted successfully."}
    return jsonify(response), 200
  else:
    response = {"success": False, "message": "User not found."}
    return jsonify(response), 404



@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
  """
  View to edit the user's selected fields.
  """
  user_id = current_user.id
  if request.method == 'POST':
    field_id = request.form.get('field')
    session['selected_field_id'] = field_id
    return redirect(url_for('edit_courses'))
  
  user_fields = UserFields.query.filter_by(user_id=user_id).all()
  fields = Fields.query.all()
  return render_template('edit.html', user_fields=user_fields, fields=fields)


@app.route('/edit_courses', methods=['GET', 'POST'])
@login_required
def edit_courses():
  """
  View to edit the user's selected courses within a field.
  """
  user_id = current_user.id
  field_id = session.get('selected_field_id')
  
  if request.method == 'POST':
    selected_courses = request.form.getlist('courses')
    
    UserFields.query.filter_by(user_id=user_id, field_id=field_id).delete()
    
    for course_id in selected_courses:
      # Check if the entry already exists
      existing_entry = UserFields.query.filter_by(user_id=user_id, field_id=field_id, course_id=course_id).first()
      if not existing_entry:
        new_user_field = UserFields(user_id=user_id, field_id=field_id, course_id=course_id)
        db.session.add(new_user_field)
    
    db.session.commit()
    return redirect(url_for('account'))
  
  selected_field = Fields.query.get(field_id)
  courses = Courses.query.filter_by(field_id=field_id).all()
  return render_template('edit_courses.html', field=selected_field, courses=courses)



@app.route("/my_resources")
@login_required
def my_resources():
  data = request.get_json(data)
  user_resource = UserResources(user_id=data['user_id'], resource_id=data['resource_id'])
  db.session.add(user_resource)
  db.session.commit()


@app.route("/save_resource", methods=["POST"])
@login_required
def save_resource():
  data = request.get_json()
  user_id = current_user.id
  resource_id = data['resource_id']

  existing_entry = UserResources.query.filter_by(user_id=user_id, resource_id=resource_id).first()

  if existing_entry:
    return jsonify({"success": False, "message": "Resource already saved."}), 400

  new_user_resource = UserResources(user_id=user_id, resource_id=resource_id)
  db.session.add(new_user_resource)
  db.session.commit()
    
  return jsonify({"success": True, "message": "Resource saved successfully."}), 200


@app.route("/delete_resource", methods=["POST"])
@login_required
def delete_resource():
  data = request.get_json()
  resource_id = data.get('resource_id')

  if resource_id:
    user_resource = UserResources.query.filter_by(user_id=current_user.id, resource_id=resource_id).first()
    if user_resource:
      db.session.delete(user_resource)
      db.session.commit()
      return jsonify(success=True), 200
    else:
      return jsonify(success=False, message="Resource not found"), 404

  return jsonify(success=False, message="Invalid request"), 400


@app.route("/saved_resources")
@login_required
def saved_resources():
  user_id = current_user.id
  user_resources_dict = {}

  # Query user saved resources
  user_resources = db.session.query(UserResources, Resources, Courses).join(
      Resources, UserResources.resource_id == Resources.id).join(
      Courses, Resources.course_id == Courses.id).filter(
      UserResources.user_id == user_id).all()

  # Organize resources by course name
  for ur, res, course in user_resources:
    if course.course_name not in user_resources_dict:
      user_resources_dict[course.course_name] = []
    user_resources_dict[course.course_name].append(res)

  return render_template("saved_resources.html", title="Saved Resources", user_resources=user_resources_dict)



@app.route("/add_resource", methods=['GET', 'POST'])
@login_required
def add_resource():
  """
  View to add a new resource.
  """
  user_id = current_user.id
  courses = []
  form = AddResourceForm()

  if form.validate_on_submit():
    link = form.link.data
    comment = form.comment.data

    user_fields = UserFields.query.filter_by(user_id=user_id).all()
    user = User.query.get_or_404(user_id)

    for course in list(user_fields):
      courses.append(course.courses)

    video = get_video_details(link)
    if video:
      valid_course = False
      for course in courses:
        if course.course_name.split()[0].lower() in video['title'].lower().split():
          valid_course = True
          break

      if not valid_course:
        flash('The link you provided does not correspond to any courses that you chose', 'danger')
        return redirect(url_for('add_resource'))

      resource = Resources.query.filter_by(url=video['video_url']).first()
      if resource:
        flash("The Resource already exists", "success")
        return redirect(url_for('add_resource'))

      new_resource = Resources(
        user_id=user_id,
        title=video['title'],
        url=video['video_url'],
        description=comment,
        thumbnail=video['thumbnail'],
        course_id=course.id
      )

      db.session.add(new_resource)
      db.session.commit()

      resource = Resources.query.get_or_404(new_resource.id)

      return render_template("view_resource.html", title="View Resource", user=user, resource=resource)

  return render_template("add_resource.html", title="Add Resource", form=form)


@app.route("/view_resource_info/<int:resource_id>")
@login_required
def view_resource_info(resource_id):
  resource = Resources.query.get_or_404(resource_id)
  user = User.query.get_or_404(resource.user_id)
  return render_template("view_resource.html", title="Resource Information", user=user, resource=resource)


@app.route("/profile/<int:user_id>")
@login_required
def view_profile(user_id):
  fields, courses = set(), set()
  
  user = User.query.get_or_404(user_id)
  user_fields = UserFields.query.filter_by(user_id=user_id).all()

  for field in user_fields:
    fields.add(field.fields.field_name)

  for course in user_fields:
    courses.add(course.courses.course_name)
  
  fields_length = len(fields)
  courses_length = len(courses)

  image_file = url_for('static', filename='images/' + user.image_file)

  if user_id == current_user.id:
    return redirect(url_for('account'))

  return render_template('profile.html', title='Profile', image_file=image_file, user=user, courses=courses, fields=fields, fields_length=fields_length, courses_length=courses_length)


@app.route("/peers")
@login_required
def peers():
  current_user_id = current_user.id
  user_courses = UserFields.query.filter_by(user_id=current_user_id).all()
  shared_users = set()

  for user_course in user_courses:
    course_id = user_course.course_id
    users_in_course = UserFields.query.filter_by(course_id=course_id).all()
    for user_field in users_in_course:
      if user_field.user_id != current_user_id:
        shared_users.add(user_field.user)

  return render_template('peers.html', title="Peers", shared_users=shared_users)


@app.route('/resource/<int:resource_id>/comments', methods=['GET', 'POST'])
@login_required
def resource_comments(resource_id):
  resource = Resources.query.get_or_404(resource_id)
  reviews = Reviews.query.filter_by(resource_id=resource_id).all()

  if request.method == 'POST':
    review_text = request.form.get('review')
    new_review = Reviews(user_id=current_user.id, resource_id=resource_id, review=review_text)
    db.session.add(new_review)
    db.session.commit()
    flash('Your comment has been added!', 'success')
    return redirect(url_for('resource_comments', title="Comments", resource_id=resource_id))

  return render_template('comments.html', title="Comments", resource=resource, reviews=reviews)


@app.route('/reply/<int:review_id>', methods=['POST'])
@login_required
def add_reply(review_id):
  review = Reviews.query.get_or_404(review_id)
  reply_text = request.form.get('reply')
  new_reply = Reply(user_id=current_user.id, review_id=review_id, reply=reply_text)
  db.session.add(new_reply)
  db.session.commit()
  flash('Your reply has been added!', 'success')
  return redirect(url_for('resource_comments', resource_id=review.resource_id))




