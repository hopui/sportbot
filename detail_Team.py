import urllib.request
from bs4 import BeautifulSoup


def detail_team(text):
    url = "https://sports.media.daum.net/sports/worldsoccer/"
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")

    team_num = []
    cat = ['순위 : ', '승 : ', '무 : ', '패 : ', '득실 : ', '승점 : ']
    league = ['epl', 'bundesliga', 'primera', 'seriea']
    dic = {}

    for l in league:
        teams = soup.find_all("tbody", {"data-key": l})
        for i in teams:
            details = i.get_text().split("\n")
            details = details[2:]

            for num in range(len(details)):
                team = []
                n = 0
                for k in details[num * 9: num * 9 + 9]:
                    if k is not '':
                        if k == details[num * 9 + 1]:
                            name = k
                        else:
                            team.append(cat[n] + k)
                            n += 1
                if name in dic.keys():
                    pass
                else:
                    dic[name] = team

    if text in dic.keys():
        team_num.append("#" + text)
        for t in dic[text]:
            team_num.append(t)
        # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
        return u'\n'.join(team_num)
    else:
        return u'팀명을 다시 확인해 주세요!'
