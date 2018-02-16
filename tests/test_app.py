import sys
sys.path.append('..')
import unittest
import os
from app.models import db, User
import tempfile
import pytest
from app import app


class AppTestCase(unittest.TestCase):
	"""represents the app testcase, will be called before every test"""

	def setUp(self):
		''' creates a new test client and initilise a new database'''

		app.testing = True
		self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		''' will be called after every test'''

		os.close(self.db_fd)
		os.unlink(app.config['DATABASE'])



	def test_user_registration(self):
		""" tests a user is registered on the app"""

		result = self.app.post('/', data = dict(username = 'test', email = 'test@test.com', password = '12345'))
		self.assertEqual('200 OK',result.status)


if __name__ == '__main__':
	unittest.main()
