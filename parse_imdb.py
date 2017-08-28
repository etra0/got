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

# I downloaded the page an saved as data.html
soup = BeautifulSoup(open("data.html"), "html.parser")

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
    db.write("actor;season_1;season_2;season_3;season_4;season_5;season_6;season_7\n")
    for character in characters:
        db.write("{0};{1}\n".format(
            character,
            ";".join(list(map(float_to_time, characters[character])))))
