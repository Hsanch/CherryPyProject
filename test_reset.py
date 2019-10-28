import unittest
import requests
import json

class TestReset(unittest.TestCase):

	SITE_URL = 'http://127.0.0.1:8000' #replace with your port number
	RESET_URL = SITE_URL + '/reset/'

	def test_reset_data(self):
		m = {}
		r = requests.put(self.RESET_URL)

if __name__ == "__main__":
	unittest.main()

