""" views.py"""
from functools import wraps
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.models import db, User, Business, Review



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'not_secret_any_more'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/weconnect"

db.app = app
db.init_app(app)# connecting sqlalchemy object to the app

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session and 'Myuser_id':
			return f(*args, **kwargs)
		else:
			flash("you need to login first")
			return redirect(url_for('login'))
	return wrap


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

		flash('New user registered!')
		return redirect(url_for('login'))

	return render_template('signup.html',error = error)

@app.route('/logout')
def logout():
	""" routes logs out the user"""

	session.pop('logged_in', None)
	flash('you have logged out!')
	return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
	"""route logins a user, to access the app"""

	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		myuser = User.query.filter_by(username = username).first()

		if not myuser:
			error = "username or password is incorrect, check and try again!"
        #check if it the right password passed
		if check_password_hash(myuser.password, password):
			session['logged_in'] = True
			myuser_id = myuser.id
			return redirect(url_for('viewbusiness'))

		error = "invalid username or password!"
	return render_template('login.html',error = error)


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
