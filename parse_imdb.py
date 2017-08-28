from bs4 import BeautifulSoup
from html import unescape
import re
import requests as r

def time_to_float(time):
    time = time.split(":")
    if len(time) == 1:
        return int(time[0])
    else:
        hours, minutes = time
        if not hours:
            hours = 0
        return int(hours) + int(minutes)/60

def float_to_time(value):
    if value >= 1:
        minute = int((value % int(value))*60)
        hour = int(value)
        return "{0}:{1}".format(hour, minute)
    else:
        return "0:{0}".format(int(value*60))

def generate_csv():
    """
    Generates a CSV with the name of the character, the chapter of their
    death and the hours in every season
    """

    soup = BeautifulSoup(r.get('http://imdb.com/list/ls076752033/').text, "html.parser")

    mydivs = soup.find_all("div", class_=["info", "description"])[1:]

    name_regex = re.compile(r">(.*?)</a>")

    season_regex = re.compile(r"\* [Ss]eason (\d):.*<(.*)>")

    characters = dict()
    for div in mydivs:
        if div.a:
            text = str(unescape(div.a))
            character = name_regex.findall(text)[0]
            characters[character] = [0, 0, 0, 0, 0, 0, 0]
        else:
            for children in div.children:
                if "NavigableString" in type(children).__name__:
                    text = str(children)
                    duration = season_regex.findall(text)
                    if duration:
                        season, time = duration[0]
                        characters[character][int(season) - 1] += time_to_float(time)


    with open("all_seasons.csv", "w") as db:
        db.write("actor,death,season_1,season_2,season_3,season_4,season_5,season_6,season_7\n")
        for character in characters:
            print("current: %s" % character, flush=True)
            db.write("{0},{1},{2}\n".format(
                character,
                is_dead(character),
                ",".join(list(
                    map(float_to_time, characters[character])))
                    )
                )


def parse_chapter_page(url):
    """
    Parse the page of a chapter getting the season and the chapter
    in the format SxxExx
    """
    page_request = r.get('http://gameofthrones.wikia.com%s' % url)
    if page_request.status_code == 200:
        page_text = page_request.text
    else:
        print("No se pudo encontrar %s" % name.replace("_", " "))
        return None

    bs = BeautifulSoup(page_text, 'html.parser')
    # left column of gameofthrones.wikia
    mydivs = bs.find_all("td",
        class_=["pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing"])

    season, episode = (None, None)
    for tag in  mydivs:
        if 'Season' in tag.text:
            season = int(tag.text.replace("Season ", ""))
        if 'Episode' in tag.text:
            episode = int(tag.text.replace("Episode ", ""))

    if not season or not episode:
        print("check this one")
        return "S00E00"

    return "S%02dE%02d" % (season, episode)

def is_dead(name):
    """
    If the character is dead, returns the chapter of his death.
    If not, returns None
    """
    if name == 'Grand Maester Pycelle':
        name = 'Pycelle'

    # removing nickname to search in gameofthrones.wikia
    nickname_regex = re.compile("'.*?' ?")
    name = nickname_regex.sub("", name)
    name = name.replace(" ", "_")

    page_request = r.get('http://gameofthrones.wikia.com/wiki/%s' % name)
    if page_request.status_code == 200:
        page_text = page_request.text
    else:
        print("No se pudo encontrar %s" % name.replace("_", " "))
        return None

        
    bs = BeautifulSoup(page_text, 'html.parser')
    # left column of gameofthrones.wikia
    mydivs = bs.find_all("div", \
        class_=["pi-item pi-data pi-item-spacing pi-border-color"])

    dead = False
    for div in mydivs:
        for tag in div:
            if tag.name == 'h3' and tag.text == 'Death':
                # print("%s:  ☠️" % name.replace("_", " "), end=' ')
                dead = True
                continue

            if dead and tag.name == 'h3' and tag.text == 'Death shown in episode':
                # we need to do this twice cause reasons.
                tag = tag.next_sibling
                tag = tag.next_sibling
                return parse_chapter_page(tag.a['href'])


    if not dead:
       return None


generate_csv()

