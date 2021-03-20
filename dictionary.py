import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request

class __Dictionary():
    def __init__(self, wordSoup):
        self.wordSoup = wordSoup
        self.name = None
        self.definitions = None
        self.partOfSpeech = None

    def getDefinitions(self):
        if self.wordSoup == "404": return "Page cannot be found"

        definitions = self.wordSoup.findAll("span", {"class": "one-click-content css-ibc84h e1q3nk1v1"})

        if len(definitions) == 0: return "No definitions found"

        return definitions

    def getPartOfSpeech(self):
        pass

class Word(__Dictionary):
    def __init__(self, wordSoup, name):
        super().__init__(wordSoup)
        self.name = name

    def definitions(self):
        pass

    def partOfSpeech(self):
        pass

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
        return "404"

    wordSoup = soup(pageHtml, "html.parser")

    word = Word(wordSoup=wordSoup) 


