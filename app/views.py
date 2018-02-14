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
def load_user(user_id):
	""" loads user from an id from the database"""
	return User.query.get(int(user_id))

login_manager.login_view = 'login'




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

		user = User.query.filter_by(username = username).first()

		if not user:
			error = "username or password is incorrect, check and try again!"
			return render_template('login.html', error = error)
        #check if it the right password passed
		if check_password_hash(user.password, password):

			login_user(user)
			flash('Logged in successfully!')
			return redirect(url_for('viewbusiness'))

		error = "invalid username or password!"
	return render_template('login.html',error = error)


@app.route('/logout')
@login_required
def logout():
	""" routes logs out the user"""

	logout_user()
	flash('logged out successfully!')
	return redirect(url_for('login'))



@app.route('/business')
@login_required
def viewbusiness():
	""" routes enables user to see registered businesses """

	all_businesses = Business.query.all()
	return render_template('business.html',businesses = all_businesses, current_user = current_user)


@app.route('/addbusiness', methods = ['POST','GET'])
@login_required
def addbusiness():
	""" route enables user add a business"""

	error = None
	if request.method == 'POST':
		name = request.form['business_name']
		category = request.form['category']
		location = request.form['location']

		business = Business.query.filter_by(business_name = name, business_category = category, business_location = location).first()
		if business:
			error = 'Business already exists!'
			return render_template('addBusiness.html', error = error)

		newbusiness = Business(business_name = name, business_category = category, business_location = location, user_id = current_user.id)
		db.session.add(newbusiness)
		db.session.commit()

		flash('new business added!')
		return redirect(url_for('viewbusiness'))
	return render_template('addBusiness.html', error = error)


@app.route('/updatebusiness', methods = ['POST'])
@login_required
def update_business():
	"""route enables authenticated user update a business they created """

	business = Business.query.filter_by(id = request.form['id']).first()
	business.business_name = request.form['business_name']
	business.business_category = request.form['category']
	business.business_location = request.form['location']
	business.user_id = request.form['user_id']

	if business.user_id == current_user.id:
		db.session.commit()
	error = 'you dont have permission to edit!'

	return render_template('business.html', error = error)

@app.route('/deletebusiness')
@login_required
def delete_business():
	'''routes allows a user that created a business to delete it '''

	business = Business.query.filter_by(id = request.form['id']).first()
	business.user_id = request.form['user_id']

	if business.user_id == current_user.id:
		db.session.delete(business)

	error = 'you dont have permission to delete!'
	return render_template('business.html', error = error)


@app.route('/reviews')
@login_required
def reviews():
	""" routes enables users view reviews about businesses"""

	return render_template('reviews.html')
