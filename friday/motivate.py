import requests
class Motivate(object):
	def __init__(self):
		self.data = requests.get('http://quotes.rest/qod.json').json()
		self.quote = self.data['contents']['quotes'][0]

	def get_quote(self):
		return "\"*" + self.quote['quote'] + '*"\n -by ' + '**' + self.quote['author'] + '**'
