# import pprint
# import requests

# class Joke():
#     def tellJoke(self):
#         joke=requests.get('https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke').json()
#         print(joke["setup"])
#         print(joke["punchline"])
#         result='**'+joke["setup"]+'**'+'\n'+'Answer : '+ joke["punchline"]
#         return result


import requests

class Joke():
    def tellJoke(self):
        url = "https://joke3.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': "d77247d9d5mshcd80fe022df2190p147e3ejsne294efd57b74"
            }

        joke = requests.request("GET", url, headers=headers)

        print(joke.json()['content'])
        return joke.json()['content']