from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='d34d3205f0794f85af841f72c04abd06')


#d34d3205f0794f85af841f72c04abd06
class Hackernews(object):
	def __init__(self):
		pass

	def get_hackernews(self, topic):
		response = ''

		if(topic == 'coronavirus'):
			x = newsapi.get_top_headlines(q=topic)

		elif topic == 'coronavirus india':
			x = newsapi.get_top_headlines(q=topic, sources='the-hindu, the-times-of-india, google-news-in')
						
		
		for i in x['articles']:
			response +=i['description'] + "\n" + i['url'] + '\n\n'
		return response