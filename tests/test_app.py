import sys
sys.path.append('..')
import unittest
import app
from app.models import db

class AppTestCase(unittest.TestCase):
	"""represents the app testcase, will be called before every test"""

	def setUp(self):
		''' creates a new test client and initilise a new database'''
		self.app = app.test_client()
		app.testing = True
		db.create_all()

		self.user = User(username = 'test', email = 'test@test.com', password = '12345')
		db.session.add(user)
		db.session.commit()

	def tearDown(self):
		''' will be called after every test'''

		db.session.remove()
		db.drop_all()



if __name__ == '__main__':
	unittest.main()
