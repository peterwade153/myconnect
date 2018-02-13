""" views.py"""
from functools import wraps
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import app
from app.models import db, User, Business, Review



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'not_secret_any_more'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/weconnect"

db.app = app
db.init_app(app)# connecting sqlalchemy object to the app

#creating an instance of login manager and initializing it with our app instance
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
	""" loads user from an id from the database"""
	return User.query.get(int(id))

login_manager.login_view = 'login'


@app.before_request
def before_request():
	""" runs before view function each time a request is recieved. will store logged in user"""

	g.user = current_user


@app.route('/', methods=['POST', 'GET'])
def signup():
	"""route registers a new user on the application"""

	error = None
	if request.method == "POST":
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']

		#check if user doesnt exist!
		new_user = User.query.filter_by(username = username).first()
		if new_user:
			error = "User already exists!"
			return render_template('signup.html', error = error)

		myuser = User(username = username, email = email, password = password)
		db.session.add(myuser)
		db.session.commit()

		flash('User registered successfully!')
		return redirect(url_for('login'))
	return render_template('signup.html',error = error)



@app.route('/login', methods=['POST', 'GET'])
def login():
	"""route logins a user, to access the app"""

	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		myuser = User.query.filter_by(username = username, password = password).first()

		if not myuser:
			error = "username or password is incorrect, check and try again!"
        #check if it the right password passed
		if check_password_hash(myuser.password, password):

			login_user(myuser)
			flash('LOgged in successfully!')
			return redirect(url_for('viewbusiness'))

		error = "invalid username or password!"
	return render_template('login.html',error = error)


@app.route('/logout')
def logout():
	""" routes logs out the user"""

	logout_user()
	return redirect(url_for('login'))



@app.route('/business')
@login_required
def viewbusiness():
	""" routes enables user to see registered businesses """

	all_businesses = Business.query.all()
	return render_template('business.html',businesses = all_businesses)

@app.route('/addbusiness')
@login_required
def addbusiness():
	""" route enables user add a business"""

	return render_template('addBusiness.html')

@app.route('/reviews')
@login_required
def reviews():
	""" routes enables users view reviews about businesses"""

	return render_template('reviews.html')
