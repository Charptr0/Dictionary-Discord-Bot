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

getSynonyms() sort all synonyms into a list
    - return a list of all synonyms

getAntonyms() sort all antonyms into a list
    - return a list of all antonyms

getUrbanDefinitions() sorts all urban definitions into a list
    - return a list of all urban definitions

getContributor() sort all contributors into a list
    - return a list of all contributors

delete()
    - delete the instance
'''
class __Dictionary():
    def __init__(self, wordSoup):
        self._wordSoup = wordSoup 
        self._name = None
        self._main_definitions = None
        self._partOfSpeech = None
        self._LIMIT = 3 #this set how many definitions the bot is going to show
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

    def _getUrbanDefinitions(self) -> list:
        list_of_all_urban_definitions = self._wordSoup.findAll("div", {"class" : "meaning"})
        
        return list_of_all_urban_definitions

    def _getContributor(self) -> list:
        list_of_all_contributor = self._wordSoup.findAll("div", {"class" : "contributor"})
        
        return list_of_all_contributor

    def delete(self):
        del self

'''
The Word class is a subclass of the Dictionary class, its function is to provide a organized way to print the 
embed messages

name()
    - return the name in strings

definitions()
    - grab the list of all sorted defintions
    - sort them into strings according to the _LIMIT
    - return the definitions as a string

partOfSpeech()
    - grab the list of all sorted part of speech
    - grab the first element of that list
    - return the part of speech as a list

synonyms()
    - grab the list of all sorted synonyms
    - sort them into strings according to the _LIMIT
    - return the synonyms as a string

antonyms()
    - grab the list of all sorted antonyms
    - sort them into strings according to the _LIMIT
    - if there are no antonyms, return NONE
    - return the antonyms as a string
'''

class Word(__Dictionary):
    def __init__(self, wordSoup, name):
        super().__init__(wordSoup)
        self._name = name

    def name(self) -> str: return self._name

    def definitions(self) -> str:
        list_of_all_definitions = self._getDefinitions() #Grab the list of definitions from the dictionary class
        if len(list_of_all_definitions) == 0: return "No definitions found" #if the length of the list is 0, then no definition is found by the program

        self._main_definitions = "" 

        for index, definition in enumerate(list_of_all_definitions):
            if index == self._LIMIT: break
            self._main_definitions += "{}. {}\n".format((index+1), definition.text)
        
        return self._main_definitions

    def partOfSpeech(self) -> str:
        self._partOfSpeech = (self._getPartOfSpeech())[0].text
        return str(self._partOfSpeech)

    def synonyms(self) -> str:
        list_of_all_synonyms = self._getSynonyms()

        self._synonyms = ""

        for index, synonym in enumerate(list_of_all_synonyms):
            if index == self._LIMIT: break
            self._synonyms += "{}. {}\n".format((index+1), synonym.text)

        return self._synonyms

    def antonyms(self) -> str:
        list_of_all_antonyms = self._getAntonyms()

        if len(list_of_all_antonyms) == 0: return None #if no antonyms exist for that word

        self._antonyms = ""

        for index, antonym in enumerate(list_of_all_antonyms):
            if index == self._LIMIT: break
            self._antonyms += "{}. {}\n".format((index+1), antonym.text)
        
        return self._antonyms

'''
The UrbanWord class is a subclass of the Dictionary class, its function is to provide a organized way to print the 
embed messages

phrase()
    - return the phrase as a string

definitions()
    - grab the top definition
    - return the definition as a string

author()
    - grab the author who created the top definition and the contribution date
    - return the author's name and the contribution date as a string

'''
class UrbanWord(__Dictionary):
    def __init__(self, wordSoup, phrase):
        super().__init__(wordSoup)
        self._phrase_list = phrase
        self._author = None
    
    def phrase(self) -> str:
        complete_phrase = ""

        for index, word in enumerate(self._phrase_list):
            if index == 0:
                complete_phrase = word

            else : complete_phrase += " " + word
        
        return complete_phrase

    def definition(self) -> str:
        return self._getUrbanDefinitions()[0].text

    def author(self) -> str:
        self._author = self._getContributor()[0].text
        
        return self._author

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

'''
_getThesaurusHTML()
    - private function
    - connect to thesaurus.com using urlopen() from the request module
    - download the HTML from the page
    - beautiful soup will parse the HTML data and update the _wordsoup var
    - use this to get the antonyms ONLY

    - if request cannot get the webpage or the webpage DNE, it will return with 404
'''

def _getThesaurusHTML(word : Word):
    url = "https://www.thesaurus.com/browse/" + word.name() #the word's page on the dictionary.com

    try: #access that URL
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla'})) as webpage:
                pageHtml = webpage.read()
    except: #if some error occurs, we assume the page DNE, and terminate the function
        return "404 Webpage cannot be found"

    word._wordSoup = soup(pageHtml, "html.parser")


'''
getUrbanHTML()
    - connect to urbandictionary.com using urlopen() from the request module
    - download the HTML from the page
    - beautiful soup will parse the HTML data and return a new instance of the UrbanWord() class

    - if request cannot get the webpage or the webpage DNE, it will return with 404
'''
def getUrbanHTML(phrase : list) -> UrbanWord:
    url = "https://www.urbandictionary.com/define.php?term="

    for index, word in enumerate(phrase): #urbandictionary url formatting
        if index == 0:
            url += word
        else: url += "%20" + word
    
    try: #access that URL
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla'})) as webpage:
                pageHtml = webpage.read()
    except: #if some error occurs, we assume the page DNE, and terminate the function
        return "404 Webpage cannot be found"

    wordSoup = soup(pageHtml, "html.parser")

    newUrbanPhrase = UrbanWord(wordSoup=wordSoup, phrase=phrase) #Create a new instance of the word class
    
    return newUrbanPhrase
