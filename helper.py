from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import csv

def ltos(s):
    str1 = " " 
    return (str1.join(s)) 

def getHTML(link):
    req = requests.get(link)
    html = req.content
    return html

def heading(name):
    header = ['Title', 'ID', 'IMDB Budget', 'Cumulative Worldwide Gross', 'Opening Weekend USA', 'Gross USA', 'Cast 1' , 'Cast 2', 'Cast 3', 'Company Credits',  'TMDB Budget ($)', 'TMDB Revenue ($)', 'Cinestaan Budget (INR)', 'Cinestaan Revenue (INR)', 'Box Office India Budget (INR)', 'Box Office India Revenue (INR)', 'The Numbers Domestic Gross', 'The Numbers Worldwide Gross']
    with open(name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def tabulate(name, detail):
    array = []
    array.append(detail['title'])
    array.append(detail['id'])
    array.append(detail['imdb'][0])
    array.append(detail['imdb'][1])
    array.append(detail['imdb'][2])
    array.append(detail['imdb'][3])
    array.append(detail['imdb'][4])
    array.append(detail['imdb'][5])
    array.append(detail['imdb'][6])
    array.append(detail['imdb'][7])
    array.append(detail['thdb'][0])
    array.append(detail['thdb'][1])
    array.append(detail['cinestaan'][0])
    array.append(detail['cinestaan'][1])
    array.append(detail['boi'][0])
    array.append(detail['boi'][1])
    array.append(detail['number'][0])
    array.append(detail['number'][1])

    with open(name, 'a', encoding='UTF-8', newline='') as f:
        try:
            writer = csv.writer(f)
            writer.writerow(array)
        except:
            array[0] = 'Illegal character in title'
            writer = csv.writer(f)
            writer.writerow(array)



def movieDetail(id):
    ret_det = {}
    link = "https://www.imdb.com/title/{}".format(id)
    html = getHTML(link)
    soup = BeautifulSoup(html, "html.parser")
    
    title = soup.find("div", {"class": "title_wrapper"})
    title = title.find("h1").text
    
    ret_det["id"] = id
    title = re.sub("[\(\[].*?[\)\]]", "", title).strip()
    ret_det["title"] = title
    details = soup.find("div", {"id": "titleDetails"})
    details_str = str(details).split("<hr/>")
    box_office = ""
    for det_str in details_str:
        if "Box Office" in det_str:
            box_office = det_str
    box_office = BeautifulSoup(box_office, "html.parser")
    box_office_details = box_office.findAll("div", {"class":"txt-block"})
    
    
    cast1 = ""
    cast2 = ""
    cast3 = ""

    try:
        cast_det = soup.find("div", {"id": "titleCast"})
        casts = cast_det.findAll("tr")
        cast1 = casts[1].text.split("...")[0].strip()
        cast2 = casts[2].text.split("...")[0].strip()
        cast3 = casts[3].text.split("...")[0].strip()
    except:
        pass

    imdb_dets = ['','','','','','', '', '']

    imdb_dets[4] = cast1
    imdb_dets[5] = cast2
    imdb_dets[6] = cast3

    try:
        link = link + "/companycredits"
        html = getHTML(link)
        soup = BeautifulSoup(html, "html.parser")
        production = soup.find('div', {'id': 'company_credits_content'})
        company = production.find('ul').text.strip()
        imdb_dets[7] = company
    except:
        pass

    for box_office_detail in box_office_details:
        if box_office_detail.find('h4').text == 'Budget:':
            try:
                budget = box_office_detail.text.strip().replace("\n","").replace("Budget:","").split()[0]
                imdb_dets[0] = budget
            except:
                continue
        elif box_office_detail.find('h4').text == 'Opening Weekend USA:':
            try:
                revenue = box_office_detail.text.strip().replace("\n","").replace("Opening Weekend USA:","").strip()
                imdb_dets[1] = budget
            except:
                continue
        elif box_office_detail.find('h4').text == 'Gross USA:':
            try:
                revenue = box_office_detail.text.strip().replace("\n","").replace("Gross USA:","").strip()
                imdb_dets[2] = budget
            except:
                continue
        elif box_office_detail.find('h4').text == 'Cumulative Worldwide Gross:':
            try:
                revenue = box_office_detail.text.strip().replace("\n","").replace("Cumulative Worldwide Gross:","").strip()    
                imdb_dets[3] = revenue
            except:
                continue

    ret_det["imdb"] = imdb_dets


    thdb_dets = []
    try:
        thdb_dets = tmdb(title)
    except:
        thdb_dets.append('')
        thdb_dets.append('')
        pass
    try:
        if thdb_dets[0] == 0:
            thdb_dets[0] = ""

        if thdb_dets[1] == 0:
            thdb_dets[1] = ""
    except:
        pass
    
    ret_det["thdb"] = thdb_dets

    cine_dets = []
    try:
        cine_dets = cinestaan(title)
    except:
        cine_dets.append('')
        cine_dets.append('')
        pass
    ret_det["cinestaan"] = cine_dets

    boi_dets = []
    try:
        boi_dets = boi(title)
    except:
        boi_dets.append('')
        boi_dets.append('')
        pass
    ret_det["boi"] = boi_dets

    number_dets = []

    try:
        number_dets = numbers(title)
    except:
        number_dets.append('')
        number_dets.append('')
        pass

    try:
        if number_dets[0] == '0':
            number_dets[0] = ""
        if number_dets[1] == '0':
            number_dets[1] = ""
    except:
        pass

    ret_det["number"] = number_dets
    return ret_det
    
def boi(movie_name):
    boi_dets = [' ', ' ']
    link = "https://boxofficeindia.com/search.php?txtSearchStr={}&search_type=movies&x=15&y=15".format(movie_name)
    html = getHTML(link)

    soup = BeautifulSoup(html, "html.parser")

    res = soup.find("tr", {"class": "boi-search-rows"})
    res = res.find("a")["href"]
    res = "https://boxofficeindia.com/" + res

    html = getHTML(res)
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.findAll("div",{"class":"movieboxssec"})
    soup = soup[3]
    movie_information_table = soup.find("table",{"class":"mviedtailstbe"})
    movie_informations = movie_information_table.findAll("tr")
    for movie_information in movie_informations:
        information = movie_information.text.strip().replace("\n","").replace("\xa0","")
        if 'Budget' in information:
            boi_dets[0] = information.replace("Budget:","")
        elif 'Worldwide Gross' in information:
            boi_dets[1] = information.replace("Worldwide Gross:", "")
            break

    return(boi_dets)
    # print(res)

def tmdb(movie_name):
    thdb_dets = ['', '']
    api_key = "d3223a6ef267738935b5db9dec91a1b5"

    search_data = requests.get("https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(api_key, movie_name.replace(" ","+"))).json()
    movie_id = search_data["results"][0]["id"]
    movie_details = requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id, api_key)).json()
    budget = movie_details["budget"]
    revenue = movie_details["revenue"]
    thdb_dets[0] = budget
    thdb_dets[1] = revenue
    return thdb_dets

def cinestaan(movie_name):
    cine_dets = ['', '']
    movie_name = movie_name.replace(" ","+")
    link = "https://www.cinestaan.com/movies/{}/1/20".format(movie_name)
    html = getHTML(link)

    soup = BeautifulSoup(html, "html.parser")
    movies_section = soup.find("section",{"id": "results"})
    movie_link = movies_section.find("a")['href']
    
    html = getHTML(movie_link)
    soup = BeautifulSoup(html, "html.parser")

    movie_information = soup.find('section', {'id': 'db__movie__explore'})
    dts = movie_information.findAll('dt')
    dds = movie_information.findAll('dd')
    
    for index, dt in enumerate(dts):
        if dt.text == 'Budget':
            cine_dets[0] = dds[index].text.replace("INR ","").replace("(est.)", "").strip()
        if dt.text =='Revenue':
            cine_dets[1] = dds[index].text.replace("INR ","").replace("(est.)", "").strip()
    return (cine_dets)

def numbers(movie_name):
    numbers_dets = ['', '']
    movie_name = movie_name.replace(" ","+")
    link = "https://www.the-numbers.com/custom-search?searchterm={}&searchtype=simple".format(movie_name)
    # print(link)
    html = getHTML(link)
    
    soup = BeautifulSoup(html, "html.parser")
    try:
        chart = soup.findAll("div", {"id": "page_filling_chart"})[1]
        table = chart.find("table")
        row = table.findAll("td", {"class": "data"})
        numbers_dets[0] = row[1].text
        numbers_dets[1] = row[2].text
    except:
        return numbers_dets
    return numbers_dets

    #     print(detail.text)

def driver():
    with open('input.txt', 'r') as f:
        movies = f.readlines()
    details_array =[]
    for movie in movies:
        movie = movie.strip()
        detail = movieDetail(movie)
        pprint(detail)
        tabulate("results.csv", detail)
        details_array.append(detail)
