# coding = utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import twitterSentimentAnlaysis
import csv

__author__ = "Manoj KV"

# ------------------------------------------------------------------#
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
# ------------------------------------------------------------------#

"""
# commented out as its not required\n"
 class Actor(object):\n"
     def __init__(self, name = None, image = None, profession = None, bestwork = None):\n"
         self.name  =  name\n"
         self.image  =  image\n"
         self.profession  =  profession\n"
         self.bestwork  =  bestwork\n")
"""


def get_all_details():
    """
    *describe get_all_details function here*
    :return: *describe return value here*
    """

    url = "http://m.imdb.com/feature/bornondate/"
    # print url

    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver_win32\chromedriver.exe")
    driver.get(url)  # instruct driver to open the URL in new window
    driver.maximize_window()  # to See full size of the web page

    html_content = driver.page_source
    # print html_content

    soup = BeautifulSoup(html_content,"html.parser")
    # print soup
    # print(soup.prettify())

    section = soup.find("section","posters list")
    # print section

    poster = section.findAll("a","poster ")
    # print poster

    # celebrity_details  =  []  # Create Empty List and later append

    celebrity_json = []  # Create Empty List and later append

    for items in poster:
        # print items

        name = items.find("span","title").text
        # print "Name of the celebrity:", name

        image = items.img["src"]
        # print "Celebrity Image:", image

        details=re.split(",(?=(?:[^']*\'[^']*\')*[^']*$)",items.find("div","detail").text)
        # print details

        profession = details[0]
        # profession  =  items.find("div", "detail").text.split(',')[0]
        # print "Profession:", profession

        bestwork = details[1].strip()
        # bestwork  =  items.find("div", "detail").text.split(',')[1].strip()
        # print "Best work:", bestwork.strip()  # remove the leading and trailing white spaces
        # print '\n'

        # celebrity_details.append(Actor(name, image, profession, bestwork))
        celebrity_json.append({"name": name,"image": image,"profession": profession,"bestwork": bestwork})
    driver.close()

    # return celebrity_details
    return celebrity_json


if __name__ == '__main__':

    celebrities = get_all_details()
    sentiment = twitterSentimentAnlaysis.SentimentAnalysis()

    # for celebrity in celebrities:
    #     print celebrity.name, celebrity.bestwork, celebrity.profession, celebrity.image

    with open('imdb_celebrity_twitter_sentiment.txt', 'wb') as outfile:
        outfile.truncate()
        # writer = csv.writer(outfile, lineterminator='\r\n', quotechar="'")
        outfile.write("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" + "\n")
        outfile.write("@@@@@@@@@  Sentiment Analysis for Birthday Celebrities  @@@@@@@@" + "\n")
        outfile.write("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" + "\n\n")

        for c in range(10):
            CelebrityName = celebrities[c]["name"]
            sentiment.celebritysearch(CelebrityName)
            OverallSentiment = sentiment.sentiment()

            # Writing all the attributes to output file.
            outfile.write("Name of the celebrity: " + CelebrityName.encode("utf8") + "\n")
            outfile.write("Celebrity Image: " + celebrities[c]["image"].encode("utf8") + "\n")
            outfile.write("Profession: " + celebrities[c]["profession"].encode("utf8") + "\n")
            outfile.write("Best Work: " + celebrities[c]["bestwork"].encode("utf8") + "\n")
            outfile.write("Overall Sentiment on Twitter: " + OverallSentiment.encode("utf8") + "\n\n")

    print("Results are stored in output file 'imdb_celebrity_twitter_sentiment.txt'")
