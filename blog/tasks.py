import requests
from bs4 import BeautifulSoup

def get_zum_realtime_keywords():
    url = "https://zum.com/"

    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    tag_list = soup.select(".rank_list .keyword")
    keyword_list = []

    for tag in tag_list:
        if tag.text not in keyword_list:
            keyword_list.append(tag.text)

    return keyword_list