import pprint
import zulip
import sys
import re
import json
import httplib2
import os
import requests
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

import time

from motivate import Motivate

from dict import Dictionary

import pycountry

import threading

from hackernews import Hackernews

from joke import Joke


BOT_MAIL = "friday-bot@zulipchat.com"

def getHelloMessage(msg):
	name = msg['sender_full_name'].split()[0]
	return 'Welcome ' + name +  ', I\'m Friday Your assistant to this realm. Looking for any assistance or information?\nLet me help you out!'

def checkListContinsWords(list, words, relation):

	if relation == 'any':

		for word in words:
			for i in range(0, len(list)):
				if re.match('.*' + word + '.*', list[i]):
					return True
		else:
			return False

	elif relation == 'all':
		for word in words:
			for i in range(0, len(list)):
				if re.match('.*' + word + '.*', list[i]):
					break
			else:
				return False
		else:
			return True


	pass
countries = [x.name.lower() for x in list(pycountry.countries)]
countries[countries.index('united states')] = 'usa'
countries[countries.index('united kingdom')] = 'uk'

symptoms = ['fever', 'cough', 'difficult', 'breath', 'tire', 'fatigue']

class ZulipBot(object):

	def f(self, f_stop):

		print('timer..')

		self.client.send_message({
						"type": "stream",
						"to": 'general',
						"subject": 'swiming turtles',
						"content": 'Make sure to wash your hands.'
						})
		if not f_stop.is_set():
			# call f() again in 60 seconds
			threading.Timer(5*60, self.f, [f_stop]).start()

	def __init__(self):
		self.client = zulip.Client(site="https://nokia3310.zulipchat.com/api/")
		self.subscribe_all()
		# self.chatbot = ChatBot("Friday", trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
		# self.chatbot.train("chatterbot.corpus.english")
		
		
		self.hacknews = Hackernews()

		self.dictionary = Dictionary()
		
		
		self.joke = Joke()

		self.motivate = Motivate()
		
		
		
		self.subkeys = ["joke", "news", "motivate", "help", "hi", "hello", "hey", "stat.*", "define", ["what", "is"]]

	

	def urls(self, link):
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', link)
		return urls

	def subscribe_all(self):
		json = self.client.get_streams()["streams"]

		stream_names = [{"name": stream["name"]} for stream in json]
		self.client.add_subscriptions(stream_names)


	def help(self):
		message = "**Welcome to Friday Bot**\nFriday Bot has various subfields\nType `friday help <subfield>` to get help for specific subfield.\n"
		message += "\n**Subfields**\n"
		
		
		message += "`joke` - Get Jokes\n"

		message += "`motivate` - Get a motivational quote\n"
				
		message += "`news <topic>` - Get Top News Results about a topic\n"

		message += "`coronavirus stats` - Get the current Covid-19 global/country statistics \n"

		message += "`friday <question>`Ask any query related to coronavirus.\n"
		
		message += "\nIf you're bored Talk to Friday Bot, it will supercharge you"
		return message
	def help_sub(self, key):
		key = key
		message = "**Usage**\n"
		
		
		
		
		
		if key == "define":
			message += "`friday define <word>` - To Get Definition of the word\n"
		elif key == "joke":
			message += "`friday joke` - Get a Joke\n"
		
		
		
		
		
		
		elif key == "mustread":
			message += "`friday mustread @**<User Mention>** <message>` - Pass Important Messages to Team Members\n"
		
		
		
		
		
		
		
		elif key == "news" or key == "news":
			message += "`friday news` OR `friday hackernews` - Show Top 10 stories News\n"
		
		
		else:
			message = self.help()
			message += "\n{} is not a valid subfield\n".format(key)
		return message		

	def send(self, type, msg, message):
		
		# print('sending to:' + msg['display_recipient'][0]['email'])
		if type == 'stream':
			stream_name = stream_name = msg['display_recipient']
			stream_topic = msg['subject']
			

			self.client.send_message({
								"type": "stream",
								"to": stream_name,
								"subject": stream_topic,
								"content": message
								})
		else:
			if 'friday' in msg['display_recipient'][0]['email']:
				i=1
			else:
				i=0
			id = msg['display_recipient'][i]['email']
			self.client.send_message({
								"type": "private",
								"to": id,
								"content": message
								})
			
	def checkFriday(self, msg, type):


		content = msg["content"]

		#check for reference to friday
		if (type == 'private' and content[0] in ['hi', 'hello', 'hey']) or (len(content) > 1 and (((content[0] in ['hi', 'hello', 'hey']) and (content[1] == 'friday' or re.match('@\*\*friday.*', content[1]))) or ((content[1] in ['hi', 'hello', 'hey']) and (content[0] == 'friday' or re.match('@\*\*friday.*', content[0]))))):
			message = getHelloMessage(msg)
			self.send(type, msg, message)
			return
		elif  type == 'stream' and (content[0] == 'friday' or '**friday' in content[0]):
			if len(content) > 1:

				index = 1
			else :
				index = 0
		
		elif type == 'private':
			if (content[0] == 'friday' or '**friday' in content[0]) and len(content) > 1:
				index = 1
			else:
				index = 0
		
		else:
			return

		# #check for subkey
		# 
		# flag = 0
		# for i in range(0, len(self.subkeys)):
			
		# 	for j in range(0, len(content)):
				
		# 		if( re.match(self.subkeys[i], content[j])):
		# 			flag = 1
		# 			key = j
		# 			#set a value here as index of condition
		# 			#then replace all elifs below (enws, joke) with that index
		# 			break

		# 	if(flag == 1):
		# 		break
		# else:
		# 	return

		print('index is:' + str(index))
		message = ''
			
		if ('family' in content or True in [bool(re.match('friend.*', i)) for i in content] or True in [bool(re.match('relative.*', i)) for i in content] or checkListContinsWords(list=content, words=['brother', 'sister', 'mother', 'father', 'uncle', 'aunt', 'girlfriend', 'boyfriend', 'son', 'daughter']+['pet', 'dog', 'cat', 'mouse', 'hamster', 'monkey'], relation='any')):
			if (True in [bool(re.match('symptom.*', i)) for i in content] or True in [bool(re.match('sign.*', i)) for i in content]) or ('has' in content or 'got' in content or 'have' in content) or (checkListContinsWords(content, symptoms + ['symptom', 'coronavirus', 'covid'], 'any')):
				message = 'The symptoms of coronavirus (fever, cough, sore throat, and trouble breathing) can look a lot like illnesses from other viruses. If a family member or friend or relative has trouble breathing, go to the emergency room or call an ambulance right away.\n\nCall your doctor if someone in your family or friends or a relative has a fever, cough, sore throat, or other flu-like symptoms. If this person has been near someone with coronavirus or lived in or traveled to an area where lots of people have coronavirus, tell the doctor. The doctor can decide whether your family member:\n\n\t* can be treated at home\n\t* should come in for a visit\n\t* can have a telehealth visit\n\t* needs to be tested for coronavirus'
				self.send(type, msg, message)
				familyFlag = True
		elif checkListContinsWords(list=content, words=['has', 'have', 'show', 'display', 'visible','draw'],relation='any') and 'i' in content and (checkListContinsWords(list=content, words=symptoms.extend(['symptom', 'coronavirus', 'covid']), relation='any')):
			message = 'If you develop emergency warning signs for COVID-19 get medical attention immediately.'
			self.send(type, msg, message)
			return

		if (checkListContinsWords(list=content,words=['how', 'long', 'symptom'], relation='all') or checkListContinsWords(list=content,words=['how', 'long', 'sign'], relation='all') or checkListContinsWords(list=content,words=['when', 'will', 'symptom'], relation='all') or checkListContinsWords(list=content,words=['when', 'will', 'symptom'], relation='all')):
			message = 'The symptoms may appear 2-14 days after exposure to the virus:'
			self.send(type, msg, message)
			return

		if (content[index:index+2] == ['what', 'is']) or content[index] == 'define':

			if (True in [bool(re.match('.*coronavirus.*', i)) for i in content] or (True in [bool(re.match('.*covid.*', i)) for i in content])):
				message = 'Coronaviruses are a large family of viruses that are known to cause illness ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS) and Severe Acute Respiratory Syndrome (SARS).\nCoronaviruses are a large family of viruses that are known to cause illness ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS) and Severe Acute Respiratory Syndrome (SARS).'
				self.send(type, msg, message)
				return
			
			elif ('of' in content):
				i = content.index('of')
				word = content[i+1]
				message = word + ': ' + self.dictionary.words(word).capitalize()
				self.send(type, msg, message)
				return

			elif len(content) == index + 3:
				
				word = content[index + 2]
				message = word + ': ' + self.dictionary.words(word).capitalize()
				self.send(type, msg, message)
				return
			
			elif len(content) == index + 2:
				
				word = content[index + 1]
				message = word + ': ' + self.dictionary.words(word).capitalize()
				self.send(type, msg, message)
				return

				

			if checkListContinsWords(list=content, words=['incubation'], relation='any'):
				message = 'The symptoms may appear 2-14 days after exposure to the virus:'
				self.send(type, msg, message)
				return

		elif (content[index:index+2] == ['what', 'are']):

			if checkListContinsWords(list=content, words=['symptom', 'sign'], relation='any'):
				message = 'Common signs include respiratory symptoms, fever, cough, shortness of breath, and breathing difficulties. In more severe cases, infection can cause pneumonia, severe acute respiratory syndrome, kidney failure and even death.'
				self.send(type, msg, message)
				return

			# if (True in [bool(re.match('.*coronavirus.*', i)) for i in content] or (True in [bool(re.match('.*covid.*', i)) for i in content])):
			# 	message = 'Coronaviruses are a large family of viruses that are known to cause illness ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS) and Severe Acute Respiratory Syndrome (SARS).\nCoronaviruses are a large family of viruses that are known to cause illness ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS) and Severe Acute Respiratory Syndrome (SARS).'
			# 	self.send(type, msg, message)

		elif ( content[index] == 'can' ):

			if(True in [bool(re.match('.*transmit.*', i)) for i in content] ):
				message = 'The novel coronavirus can definitely be transmitted from an infected person to another person.'
				self.send(type, msg, message)
				return
			if(True in [bool(re.match('.*pet.*', i)) for i in content] or True in [bool(re.match('.*dog.*', i)) for i in content] or True in [bool(re.match('.*cat.*', i)) for i in content]):
				message += '\nThe answer for your pets varies. Visit: https://www.independent.co.uk/life-style/health-and-families/coronavirus-pet-dog-can-you-catch-it-transmission-a9376926.html'
				self.send(type, msg, message)
				return
			if ['no', 'symptom'] in content or ['no', 'symptoms'] in content or ('without' in content and True in [bool(re.match('.*symptom.*', i)) for i in content]):
				message = 'It is possisble for you to have Covid-19 without showing any symptoms and be able to transmit it to others.'
				self.send(type, msg, message)
				return
			if ((True in [bool(re.match('.*coronavirus.*', i)) for i in content] or (True in [bool(re.match('.*covid.*', i)) for i in content]))) and 'get' in content:
				message = 'You can catch coronavirus from others who have the virus. This happens when an infected person sneezes or coughs, sending tiny droplets into the air. These can land in the nose, mouth, or eyes of someone nearby, or be breathed in. You also can get infected if they touch an infected droplet on a surface and then touch their own nose, mouth, or eyes.'
				self.send(type, msg, message)
				return

		if 'how' in content or len([(x,y) for x,y in zip(['am', 'i'][0:],['am', 'i'][1:]) if x in content and y in content]) > 0 or len([(x,y) for x,y in zip(['i', 'am'][0:],['i', 'am'][1:]) if x in content and y in content]) > 0:
			
			
			if (('likely' in content or 'risk' in content) and ((True in [bool(re.match('.*coronavirus.*', i)) for i in content]) or (True in [bool(re.match('.*covid.*', i)) for i in content]) or 'disease' in  content or 'virus' in content or len([(x,y) for x,y in zip(['get', 'it'][0:],['get', 'it'][1:]) if x in content and y in content]) > 0 or len([(x,y) for x,y in zip(['catch', 'it'][0:],['catch', 'it'][1:]) if x in content and y in content]) > 0 or len([(x,y) for x,y in zip(['contract', 'it'][0:],['contract', 'it'][1:]) if x in content and y in content]) > 0) and (True in [bool(re.match('get.*', i)) for i in content] or True in [bool(re.match('.*contract.*', i)) for i in content] or True in [bool(re.match('catch.*', i)) for i in content] or 'from' in content)) or checkListContinsWords(list=content, words=['safe'], relation='any'):

				if 'i' in content:
					message = 'As long as you are inside your house and following quarantine.. you are safe'
					self.send(type, msg, message)
					return
				elif checkListContinsWords(list=content, words=['pet'], relation='any'):
					message = 'The answer for your pets varies. Visit: https://www.independent.co.uk/life-style/health-and-families/coronavirus-pet-dog-can-you-catch-it-transmission-a9376926.html'
					self.send(type, msg, message)
					return
				#add health worker 
				

			elif ((True in [bool(re.match('.*coronavirus.*', i)) for i in content] or (True in [bool(re.match('.*covid.*', i)) for i in content]))) and 'get' in content:
				message = 'You can catch coronavirus from others who have the virus. This happens when an infected person sneezes or coughs, sending tiny droplets into the air. These can land in the nose, mouth, or eyes of someone nearby, or be breathed in. You also can get infected if they touch an infected droplet on a surface and then touch their own nose, mouth, or eyes.'
				self.send(type, msg, message)
				return

		elif checkListContinsWords(list=content, words=['pet', 'dog', 'cat', 'mouse', 'hamster', 'monkey'], relation='any') and checkListContinsWords(list=content, words=['safe', 'danger', 'vulnerabl', 'risk'], relation='any'):
			message = 'The answer for your pets varies. Visit: https://www.independent.co.uk/life-style/health-and-families/coronavirus-pet-dog-can-you-catch-it-transmission-a9376926.html'
			self.send(type, msg, message)
			return

		if (content[index:index+2] in [['how', 'to'], ['how', 'often'], ['how', 'much'], ['how', 'is'], ['how', 'should'], ['how', 'can'], ['how', 'may'], ['how', 'could'], ['relative', 'it'], ['what', 'should'], ['what', 'can'], ['what', 'could'], ['is', 'there'], ['are', 'there'], ['should', 'i'], ['should', 'we']]):
			
			if checkListContinsWords(list=content, words=['travel', 'plan'], relation='all'):
				message = 'Is there any place abroad that’s safe to travel right now? In a nutshell, no. The novel coronavirus has spread to more than 100 countries and every continent except for Antarctica.\nI recommend you don\'t travel anywhere outside, even another state or town for atleast a few months. This is for your own safety'
				self.send(type, msg, message)
				return

			elif checkListContinsWords(list=content, words=['out'], relation='any'):
				message = 'You should not go outside for any purpose other than for groceries, washroom stuff or medical stuff and that too only once a day for a short time.\nAnd remember, don\'t go too far from your home and always carry your ID proof when out!'
				self.send(type, msg, message)
				return
			elif ('family' in content or True in [bool(re.match('friend.*', i)) for i in content] or True in [bool(re.match('relative.*', i)) for i in content]):
				if (True in [bool(re.match('symptom.*', i)) for i in content] or True in [bool(re.match('sign.*', i)) for i in content]) or ('has' in content or 'got' in content):
					if(familyFlag==True):
						familyFlag = False
					else:
						message = 'The symptoms of coronavirus (fever, cough, sore throat, and trouble breathing) can look a lot like illnesses from other viruses. If a family member or friend or relative has trouble breathing, go to the emergency room or call an ambulance right away.\n\nCall your doctor if someone in your family or friends or a relative has a fever, cough, sore throat, or other flu-like symptoms. If this person has been near someone with coronavirus or lived in or traveled to an area where lots of people have coronavirus, tell the doctor. The doctor can decide whether your family member:\n\n\t* can be treated at home\n\t* should come in for a visit\n\t* can have a telehealth visit\n\t* needs to be tested for coronavirus'
						self.send(type, msg, message)
						return
			if(True in [bool(re.match('.*prevent.*', i)) for i in content] or True in [bool(re.match('.*protect.*', i)) for i in content] ):
				message = 'Standard recommendations to reduce exposure to and transmission of a range of illnesses include maintaining basic hand and respiratory hygiene, and safe food practices  and avoiding close contact, when possible, with anyone showing symptoms of respiratory illness such as coughing and sneezing. \n#StayHomeStaySafe'
				self.send(type, msg, message)
				return

			elif((True in [bool(re.match('.*cure.*', i)) for i in content] or True in [bool(re.match('.*treat.*', i)) for i in content] or True in [bool(re.match('.*vaccin.*', i)) for i in content]) and (True in [bool(re.match('.*coronavirus.*', i)) for i in content] or (True in [bool(re.match('.*covid.*', i)) for i in content]) or len([(x,y) for x,y in zip(['the', 'disease'][0:],['the', 'disease'][1:]) if x in content and y in content]) > 0 or len([(x,y) for x,y in zip(['for', 'it'][0:],['for', 'it'][1:]) if x in content and y in content]) > 0 or len([(x,y) for x,y in zip(['the', 'virus'][0:],['the', 'virus'][1:]) if x in content and y in content]) > 0 )):
				message = 'There is no specific treatment for disease caused by a novel coronavirus. However, many of the symptoms can be treated and therefore treatment based on the patient’s clinical condition. Moreover, supportive care for infected persons can be highly effective.'
				self.send(type, msg, message)
				return

		elif checkListContinsWords(list=content, words=['motivat'], relation='any'):
			message = self.motivate.get_quote()
			self.send(type, msg, message)
			return
			
		elif content[index] == "joke" or (content[index] in ["tell", "crack", "show"] and "joke" in content[index + 1:]):
			text = self.joke.tellJoke()
			self.send(type, msg, text)	
		
		elif 'news' in content[index:]:
			print('news1')
			if  len([x for x in content[index:] if re.match('corona.*', x)]) > 0 or len([x for x in content[index:] if re.match('covid.*', x)]) > 0:
				
				print('news corona india')
				if 'india' in content[index:]:
					news = self.hacknews.get_hackernews('coronavirus india')
					self.send(type, msg, news)
					
				else:
					print('news corona')
					news = self.hacknews.get_hackernews('coronavirus')
					self.send(type, msg, news)
			
		
		
		elif content[index] == "help" and len(content) == index + 1:
			message = self.help()
			self.send(type, msg, message)
		elif content[index] == "help" and len(content) > index + 1:
			subkey = content[index + 1]
			message = self.help_sub(subkey)
			self.send(type, msg, message)

		elif (len([x for x in content[index:] if re.match('corona.*', x)]) > 0 or len([x for x in content[index:] if re.match('covid.*', x)]) > 0) and (len([x for x in content[index:] if re.match('stat.*', x)]) > 0 or len([x for x in content[index:] if re.match('statistic.*', x)]) > 0):
			j = -1
			
			for i in content:
				if i in countries:
					j = countries.index(i)
					break

			if j >=0:
				x = requests.get('https://api.covid19api.com/summary').json()
				x = x['Countries']
				for i in range(0, len(x)):
					if(x[i]['CountryCode'] == list(pycountry.countries)[j].alpha_2):
						stats = 'New Confirmed: ' + str(x[i]['NewConfirmed']) + '\nTotal Confirmed: ' + str(x[i]['TotalConfirmed']) + '\nNew Deaths: ' + str(x[i]['NewDeaths']) + '\nTotal Deaths: ' + str(x[i]['TotalDeaths']) + '\nNew Recovered: ' + str(x[i]['NewRecovered']) + '\nTotal Recovered: ' + str(x[i]['TotalRecovered'])
						self.send(type, msg,'Here are '+ countries[j][0].upper() + countries[j][1:] +'\'s statistics for today\n\n' +  stats)


			else:

				#call api
				x= requests.get('https://api.covid19api.com/world/total').json()
				stats = '\nTotal Confirmed: ' + str(x['TotalConfirmed']) + '\nTotalDeaths: ' + str(x['TotalDeaths']) + '\nTotalRecovered: ' + str(x['TotalRecovered']) #global
				# self.send(type, msg, stats)
				self.send(type, msg, 'Here are the global statistics \n\n' + stats)
				self.send(type, msg, '\n\ndone Global stats. \nFor countries stats, write: friday [country] covid19 stats')



		elif "friday" in content:
			message = "Alas! Finally you called me :blush:"
			self.send(type, msg, message)
			
		else:
			return

		
		
	def process(self, msg):
		pprint.pprint(msg)

		print('\n\n' + msg['type'] + ' - ' + (msg['display_recipient'] + ' - ' + msg['subject'] if msg['type'] == 'stream' else '') + '\n' + msg['sender_full_name'] + ' sent a message: ' + str([x.lower() for x in msg['content'].split()])  + '\n\n')

		sender_email = msg["sender_email"]
		if sender_email == BOT_MAIL:
			return 

		content = msg["content"].split()
		
		content = [x.lower() for x in content]
		content = [x.replace("?","") for x in content]
		content = [x.replace(",","") for x in content]
		content = [x.replace("!","") for x in content]

		msg['content'] = content
		
		

		if(msg['type'] == 'private'):

			type = 'private'
			self.checkFriday(msg, type)
		
		else:
			type = 'stream'
			self.checkFriday(msg, type)
		
		


f_stop = threading.Event()
def main():
	bot = ZulipBot()
	bot.f(f_stop)
	bot.client.call_on_each_message(bot.process)

if __name__ == "__main__":
	try:
		print('hi')
		main()
	except KeyboardInterrupt:
		print("Thanks for using Friday Bot. Bye!")
		sys.exit(0)