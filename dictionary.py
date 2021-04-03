import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request

'''
The Dictionary class is the master class, its function is to grab the HTML data from dictionary.com and sort them into list of definitions, 
part of speech, synonyms, and antonyms

getDefinitions() sort all definitions into a list
    - return a list of all definitions provided by dictionary.com

getPartOfSpeech() sort all part of speech into a list*
    - return a "list" of all part of speech
    - the first element is the main part of speech
    - discard the list after the first element
...
'''
class __Dictionary():
    def __init__(self, wordSoup):
        self._wordSoup = wordSoup 
        self._name = None
        self._main_definitions = None
        self._partOfSpeech = None
        self._LIMIT = 3
        self._synonyms = None
        self._antonyms = None

    def _getDefinitions(self) -> list:
        list_of_all_definitions = self._wordSoup.findAll("span", {"class": "one-click-content css-ibc84h e1q3nk1v1"})
        return list_of_all_definitions

    def _getPartOfSpeech(self) -> list:
        list_of_all_partOfSpeech = self._wordSoup.findAll("span", {"class" : "luna-pos"})
        return list_of_all_partOfSpeech
    
    def _getSynonyms(self) -> list:
        list_of_all_synonyms = self._wordSoup.findAll("a", {"class" : "luna-xref"})
        return list_of_all_synonyms

    def _getAntonyms(self) -> list:
        _getThesaurusHTML(word=self)
        list_of_all_antonyms = self._wordSoup.findAll("a", {"class" : "css-15bafsg eh475bn0"})
        
        return list_of_all_antonyms


'''
The Word class is a subclass of the Dictionary class, its function is to provide a organized way to print the 
embed messages

'''

class Word(__Dictionary):
    def __init__(self, wordSoup, name):
        super().__init__(wordSoup)
        self._name = name

    def name(self): return self._name

    def definitions(self):
        list_of_all_definitions = self._getDefinitions() #Grab the list of definitions from the dictionary class
        if len(list_of_all_definitions) == 0: return "No definitions found" #if the length of the list is 0, then no definition is found by the program

        self._main_definitions = "" 

        for index, definition in enumerate(list_of_all_definitions):
            if index == self._LIMIT: break
            self._main_definitions += "{}. {}\n".format((index+1), definition.text)
        
        return self._main_definitions

    def partOfSpeech(self):
        self._partOfSpeech = (self._getPartOfSpeech())[0].text
        return str(self._partOfSpeech)

    def synonyms(self):
        list_of_all_synonyms = self._getSynonyms()

        self._synonyms = ""

        for index, synonym in enumerate(list_of_all_synonyms):
            if index == self._LIMIT: break
            self._synonyms += "{}. {}\n".format((index+1), synonym.text)

        return self._synonyms

    def antonyms(self):
        list_of_all_antonyms = self._getAntonyms()

        if len(list_of_all_antonyms) == 0: return None

        self._antonyms = ""

        for index, antonym in enumerate(list_of_all_antonyms):
            if index == self._LIMIT: break
            self._antonyms += "{}. {}\n".format((index+1), antonym.text)
        
        return self._antonyms

        
class UrbanWord(__Dictionary):
    def __init__(self, wordSoup):
        super().__init__(wordSoup)
        self.author = None
        self.contributionDate = None




'''
getDictionaryWordHTML()
    - connect to dictionary.com using urlopen() from the request module
    - download the HTML from the page
    - beautiful soup will parse the HTML data and return a new instance of the word() class

    - if request cannot get the webpage or the webpage DNE, it will return with 404

'''
def getDictionaryWordHTML(word : str) -> Word:
    url = "https://www.dictionary.com/browse/" + word #the word's page on the dictionary.com

    try: #access that URL
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla'})) as webpage:
                pageHtml = webpage.read()
    except: #if some error occurs, we assume the page DNE, and terminate the function
        return "404 Webpage cannot be found"

    #parse the HTML
    wordSoup = soup(pageHtml, "html.parser")

    newWord = Word(wordSoup=wordSoup, name=word) #Create a new instance of the word class
    
    return newWord

def _getThesaurusHTML(word : Word):
    url = "https://www.thesaurus.com/browse/" + word.name() #the word's page on the dictionary.com

    try: #access that URL
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla'})) as webpage:
                pageHtml = webpage.read()
    except: #if some error occurs, we assume the page DNE, and terminate the function
        return "404 Webpage cannot be found"

    word._wordSoup = soup(pageHtml, "html.parser")
    