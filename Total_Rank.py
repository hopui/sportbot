
import urllib.request
from bs4 import BeautifulSoup


def total_rank(text):
    url = "https://sports.media.daum.net/sports/worldsoccer/"
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")

    dicts = {'프리미어리그': ['프리미어리그\n'], '분데스리가': ['분데스리가\n'], '라리가': ['라리가\n'], '세리에': ['세리에\n']}
    if text not in dicts.keys() :
        return False

    keys = soup.find_all("span", class_="txt_team")

    for i in range(1, 5):
        for key in range((i - 1) * 10, i * 10):
            if i == 1:  # 0,1,2,3,4,5,6,7,8,9  10
                dicts['프리미어리그'].append(str((key % 10) + 1) + '위 : ' + keys[key].get_text())
            elif i == 2:
                dicts['분데스리가'].append(str((key % 10) + 1) + '위 : ' + keys[key].get_text())
            elif i == 3:
                dicts['라리가'].append(str((key % 10) + 1) + '위 : ' + keys[key].get_text())
            elif i == 4:
                dicts['세리에'].append(str((key % 10) + 1) + '위 : ' + keys[key].get_text())

    print(dicts)
    if "프리미어리그" in text:
        return u'\n'.join(dicts['프리미어리그'])
    elif "분데스리가" in text:
        return u'\n'.join(dicts['분데스리가'])
    elif "라리가" in text:
        return u'\n'.join(dicts['라리가'])
    elif "세리에" in text:
        return u'\n'.join(dicts['세리에'])
