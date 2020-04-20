# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
from PyDictionary import PyDictionary

dictionary = PyDictionary()


class Dictionary():
    def words(self,word):

        meanings = dictionary.meaning(word)
        
        if meanings:
            result = meanings['Noun'][0]
        else:
            result = 'invalid word'

        return result