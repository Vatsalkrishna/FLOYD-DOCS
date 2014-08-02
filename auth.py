import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, send_from_directory 
from jinja2 import TemplateNotFound
from app import login_manager
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
import pymongo
import random



import forms
from libs.user import User

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates')



@auth_flask_login.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)
     	if user and flask_bcrypt.check_password_hash(user.password,request.form["password"]) and user.is_active():
			remember = request.form.get("remember", "no") == "yes"

			if login_user(user, remember=remember):
				flash("Logged in!")
				return redirect('/notes/create')
			else:
				flash("unable to log you in")

    return render_template("/auth/login.html")


@auth_flask_login.route("/register", methods=["GET","POST"])
def register():

	registerForm = forms.SignupForm(request.form)
	current_app.logger.info(request.form)

	if request.method == 'POST' and registerForm.validate() == False:
		current_app.logger.info(registerForm.errors)
		return "registration error"

	elif request.method == 'POST' and registerForm.validate():
		email = request.form['email']

		password_hash = request.form['password']

		user = User(email,password_hash)
		print user

		try:
			user.save()
			if login_user(user, remember="no"):
				flash("Logged in!")
				return redirect('/')
			else:
				flash("unable to log you in")

		except:
			flash("unable to register with that email address")
			current_app.logger.error("Error on registration")

				
	registerForm = RegisterForm(csrf_enabled=True)
	return render_template("/auth/register.html")

@auth_flask_login.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or '/admin')
    
    templateData = {}
    return render_template("/auth/reauth.html", **templateData)


@auth_flask_login.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')

@login_manager.unauthorized_handler
def unauthorized_callback():
	return redirect('/login')

@login_manager.user_loader
def load_user(id):
	if id is None:
		redirect('/login')
	user = User()
	user.get_by_id(id)
	if user.is_active():
		return user
	else:
		return None

