import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import word


def getHTML(word : str):
    url = "https://www.dictionary.com/browse/" + word

    with urlopen(Request(url, headers={'User-Agent': 'Mozilla'})) as webpage:
        pageHtml = webpage.read()

    pageSoup = soup(pageHtml, "html.parser")

    containers = pageSoup.findAll("span", {"class": "luna-pos"})

    return pageSoup



