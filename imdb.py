# coding=utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import re

__author__ = "Manoj KV"

"""
Problem Statement
IMDB provides a list of celebrities born on the current date. Below is the link:
http://m.imdb.com/feature/bornondate
Get the list of these celebrities from this webpage using web scraping (the ones that are displayed i.e top 10). You have to extract the below information:
     Name of the celebrity
     Celebrity Image
     Profession
     Best Work
Once you have this list, run a sentiment analysis on twitter for each celebrity and finally the output should be in the below format
     Name of the celebrity:
     Celebrity Image:
     Profession:
     Best Work:
    Overall Sentiment on Twitter: Positive, Negative or Neutral
"""


class Actor(object):
    def __init__(self, name=None, image=None, profession=None, bestwork=None):
        self.name = name
        self.image = image
        self.profession = profession
        self.bestwork = bestwork


def get_all_details():

    url = "http://m.imdb.com/feature/bornondate/"
    # print url

    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver_win32\chromedriver.exe")
    driver.get(url)  # instruct driver to open the URL in new window
    driver.maximize_window()  # to See full size of the web page

    html_content = driver.page_source
    # print html_content

    soup = BeautifulSoup(html_content, "html.parser")
    # print soup
    # print(soup.prettify())

    section = soup.find("section", "posters list")
    # print section

    poster = section.findAll("a", "poster ")
    # print poster

    # celebrity_details = []  # Create Empty List and later append

    celebrity_json = []  # Create Empty List and later append

    for items in poster:
        # print items

        name = items.find("span", "title").text
        # print "Name of the celebrity:", name

        image = items.img["src"]
        # print "Celebrity Image:", image

        details = re.split(",(?=(?:[^']*\'[^']*\')*[^']*$)", items.find("div", "detail").text)
        # print details

        profession = details[0]
        # profession = items.find("div", "detail").text.split(',')[0]
        # print "Profession:", profession

        bestwork = details[1].strip()
        # bestwork = items.find("div", "detail").text.split(',')[1].strip()
        # print "Best work:", bestwork.strip()  # remove the leading and trailing white spaces
        # print '\n'

        # celebrity_details.append(Actor(name, image, profession, bestwork))
        celebrity_json.append({"name": name, "image": image, "profession": profession, "bestwork": bestwork})
    driver.close()

    # return celebrity_details
    return celebrity_json

if __name__ == '__main__':

    celebrities = get_all_details()
    # for celebrity in celebrities:
    #     print celebrity.name, celebrity.bestwork, celebrity.profession, celebrity.image

    for celebrity_j in celebrities:
        print celebrity_j["name"] + ',' + celebrity_j["image"] + ',' + celebrity_j["profession"] + ',' \
              + celebrity_j["bestwork"]
