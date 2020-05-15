from bs4 import BeautifulSoup
import requests
from pprint import pprint

def getHTML(link):
    req = requests.get(link)
    html = req.content
    return html


def movieDetail_imdb(id):
    link = "https://www.imdb.com/title/{}".format(id)
    html = getHTML(link)
    soup = BeautifulSoup(html, "html.parser")
    


    details = soup.find("div", {"id": "titleDetails"})
    details_str = str(details).split("<hr/>")
    box_office = ""
    for det_str in details_str:
        if "Box Office" in det_str:
            box_office = det_str
    box_office = BeautifulSoup(box_office, "html.parser")
    box_office_details = box_office.findAll("div", {"class":"txt-block"})
    for box_office_detail in box_office_details:
        print(box_office_detail.text.strip().replace("\n",""))
    # print(box_office.text.strip())

# movieDetail_imdb("tt6751668")