import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request

'''
The Dictionary class is the master class, its function is to grab the HTML data from dictionary.com
This class also sort the definitions, part of speech, synonyms and antonyms

getDefinitions() sort all definitions into a list
...
'''
class __Dictionary():
    def __init__(self, wordSoup):
        self.wordSoup = wordSoup

    def getDefinitions(self):
        raw_definitions = self.wordSoup.findAll("span", {"class": "one-click-content css-ibc84h e1q3nk1v1"})
        return raw_definitions

    def getPartOfSpeech(self):
        raw_partOfSpeech = self.wordSoup.findAll("span", {"class" : "luna-pos"})[0]
        return raw_partOfSpeech

'''
The Word class is a subclass of the Dictionary class, its function is to provide a organized way to print the 
embed messages

'''

class Word(__Dictionary):
    def __init__(self, wordSoup, name):
        super().__init__(wordSoup)
        self.name = name
        self.main_definitions = None

    def definitions(self):
        list_of_all_definitions = self.getDefinitions() #Grab the list of definitions from the dictionary class
        if len(list_of_all_definitions) == 0: return "No definitions found" #if the length of the list is 0, then no definition is found by the program

        self.main_definitions = "" 

        for index, definition in enumerate(list_of_all_definitions):
            if index == 3: break
            self.main_definitions += "{}. {}\n".format((index+1), definition.text)
        
        return self.main_definitions

    def partOfSpeech(self):
        return str(self.getPartOfSpeech().text)


class UrbanWord(__Dictionary):
    def __init__(self, wordSoup):
        super().__init__(wordSoup)
        self.author = None
        self.contributionDate = None


def getHTML(word : str):
    url = "https://www.dictionary.com/browse/" + word

    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla'})) as webpage:
                pageHtml = webpage.read()
    except:
        return "404 Webpage cannot be found"

    wordSoup = soup(pageHtml, "html.parser")

    newWord = Word(wordSoup=wordSoup, name=word)
    
    return newWord


