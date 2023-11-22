#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs

WEEKLY_MEAL_URL = 'http://www.bufs.ac.kr/bbs/my/ajax.view.skin.php?bo_table=weekly_meal&wr_id=1'

def main():
    page = requests.get(WEEKLY_MEAL_URL)
    if page.status_code != 200:
        print(f"웹 페이지가 {page.status_code}를 반환했습니다")
        return -1

    soup = bs(page.text, "lxml")
    # tbls = soup.select('table.__se_tbl')
    tbls = soup.find_all('table', class_='__se_tbl')

    # 첫 번째는 운영시간, 마지막은 교직원식당임
    for idx, item in enumerate(tbls[1:-1]):
        # * 각 행을 추출한다
        tr = item.find_all('tr')

        # * 제목을 찾는다
        title_td = tr[0].find('td', colspan=3)
        if title_td:
            # print(title_td)
            title = title_td.find_all(recursive=False)[-1]

        if title:
            print(f" -*- {title.text.strip()} -*- ")

        # * 조식
        BREAKFAST_START_TR = 1
        # breakfast = tr[BREAKFAST_START_TR]  # 조식 첫 번째 행
        breakfast_td = tr[BREAKFAST_START_TR].find('td')  # 조식 첫 번째 행 첫 번째 열
        breakfast_count = int(breakfast_td.get('rowspan') or 1)

        for i in range(breakfast_count):
            menu_row = tr[BREAKFAST_START_TR+i]
            menu_td = menu_row.find_all('td')
            corner = menu_td[-2].find(recursive=True)
            menu = menu_td[-1].find(recursive=True)

            print(f'(조식) {corner.text.strip() or "CORNER ?"} : {menu.text.strip() or "???"}')

        
        # * 중식/석식
        LUNCH_START_TR = BREAKFAST_START_TR + breakfast_count
        lunch_td = tr[LUNCH_START_TR].find('td')  # 조식 첫 번째 행 첫 번째 열 (lunch_count 세는 데 필요)
        lunch_count = int(lunch_td.get('rowspan') or 1)

        for i in range(lunch_count):
            menu_row = tr[LUNCH_START_TR + i]
            menu_td = menu_row.find_all('td')

            if i == 0:
                menu = menu_td[-1].find(recursive=True).text.strip()
                corner = menu_td[-2].find(recursive=True).text.strip()
            else:
                # menu_td는 최소 1개 이상이 존재하며, -1은 항상 메뉴명
                menu = menu_td[-1].find(recursive=True).text.strip() 
                # menu_td가 2개일 경우, 첫 번째에는 코너가 오게 됨. 1개일 경우 메뉴명.
                corner_candidate = menu_td[0].find(recursive=True).text.strip()
                print(corner_candidate)
                if corner_candidate != menu:
                    corner = corner_candidate

            print(f'{corner or "CORNER ?"} : {menu or "???"}')




if __name__ == "__main__":
    main()