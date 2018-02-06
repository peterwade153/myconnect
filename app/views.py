from app import app
from app.models import db, User, Business, Reviews
from werkzeug.security import check_password_hash
from functools import wraps
from flask import render_template, request, redirect, url_for, session

db.app = app
db.init_app(app)# connecting sqlalchemy object to the app

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/weconnect"
app.config['SECRET_KEY'] = 'not_secret_any_more'


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("you need to login first")
			return redirect(url_for('login'))


@app.route('/', methods=['POST','GET'])
def signup():
	"""route registers a new user on the application"""

	error = None
	if request.method == "POST":
		Username = request.form['username']
		Email = request.form['email']
		Password = request.form['password']

		if not Username and not Email and not Password:
			error = "please all fields are required!"
			return redirect(url_for('signup'))

		#check if user doesnt exist!
		New_user = User.query.filter_by(username = Username).first()
		if New_user:
			error = "User already exists!"

		Myuser=User(username = Username, email = Email, password = Password)
		db.session.add(Myuser)
		db.session.commit()

		flash ('New user registered!')
		return redirect(url_for('login'))

	return render_template('signup.html', error=error)

@app.route('/login', methods=['POST','GET'])
def login():
	"""route logins a user, to access the app"""

	error = None
	if request.method == 'POST':
		Username = request.form['username']
		Password = request.form['password']

		Myuser = User.query.filter_by(username = Username, password = Password).first()

		if not Myuser:
			error = "username or password is incorrect, check and try again!"
        #check if it the right password passed
		if check_password_hash(Myuser.password, Password):
			session['logged_in'] = True
			Myuser_id = Myuser.id
			return redirect(url_for('viewbusiness', Myuser_id))

		error = "invalid username or password!"

	return render_template('login.html')

@app.route('/logout')
def logout():
	""" routes logs out the user"""

	session.pop('logged_in', None)
	flash('you have logged out!')
	return redirect(url_for('login'))


@app.route('/business')
@login_required
def viewbusiness(Myuser_id):
	""" routes enables user to see registered businesses """
	Current_user={}
	Current_user[id] = Myuser_id

	All_businesses = Business.query.all()
	return render_template('business.html', businesses = All_businesses)

