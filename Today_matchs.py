from Today_matchs import *
from bs4 import BeautifulSoup
from selenium import webdriver

# 크롬 드라이버 설정    # 사용자 호출 전에 실행되어야 할 것
driver = webdriver.Chrome(r'C:\Users\student\Desktop\chromedriver_win32\chromedriver.exe')


def today_match(text):
    url_text = text
    league_name = {'프리미어리그':'epl', '분데스리가':'bundesliga', '라리가':'primera', '세리에A':'seria'}
    driver.get('https://sports.news.naver.com/wfootball/schedule/index.nhn?category='+league_name[url_text])

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    today = soup.find_all("tr", class_="today")

    day = []
    res = []
    sche = {'date': '', 'time': [], 'name': [], 'place': [], 'score': [], 'image': []}

    for i in today:
        sche['date'].append(i.get_text().split('\n')[3])
        day.append(i.get_text().split('\n')[3])

    for i in today:
        for time in i.find_all("span",class_="time"):
            sche['time'].append(time.get_text())
        for name in i.find_all("span",class_="name"):
            sche['name'].append(name.get_text())
        for place in i.find_all("span",class_="place"):
            sche['place'].append(place.get_text())
        for score in i.find_all("span",class_="score"):
            sche['score'].append(score.get_text())

    res.append(0)
    res.append(sche)

    if len(sche['time']) ==0:
        return u'오늘 일정이 없습니다'
    else:
        return res
