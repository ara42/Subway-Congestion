import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep

def route(st1, st2, d, h, m):
    driver = webdriver.Chrome()
    driver.set_window_position(0,0) 
    driver.set_window_size(1920, 1000)
    driver.implicitly_wait(10)
    driver.get("https://map.kakao.com/?target=subway&REGION=01")

    sleep(13)
    driver.find_element(By.XPATH, '/html/body/div[10]/div').click()

    ##########출발역 입력
    elem = driver.find_element(By.ID, 'info.subway.searchBox.origin')
    elem.clear()
    elem.send_keys(st1)
    elem.send_keys(Keys.RETURN)

    ##########도착역 입력
    elem2 = driver.find_element(By.ID, 'info.subway.searchBox.dest')
    elem2.clear()
    elem2.send_keys(st2)
    #elem2.send_keys(Keys.RETURN)

    ##########요일 선택
    if d == "토":
        d = "토요일"
    elif d == "일":
        d = "휴일"
    else:
        d = "평일"
    
    select_element = driver.find_element(By.XPATH, '//*[@id="info.subway.searchBox.dayBox"]')
    select_element.send_keys(Keys.ENTER)

    days = driver.find_elements(By.CSS_SELECTOR, '#info\.subway\.searchBox\.listBox > li')
    for day in days:
        title = day.find_element(By.CSS_SELECTOR, 'a')
        title2 = title.get_attribute('innerText') 
        if title2 == d:
            title.send_keys(Keys.ENTER)
            break

    ##########시간 선택(hour)
    select_element = driver.find_element(By.XPATH, '//*[@id="info.subway.searchBox.hourBox"]')
    select_element.send_keys(Keys.ENTER)

    hours = driver.find_elements(By.CSS_SELECTOR, '#info\.subway\.searchBox\.listBox > li')
    for hour in hours:
        title = hour.find_element(By.CSS_SELECTOR, 'a')
        title2 = title.get_attribute('innerText')
        if title2 == h:
            title.send_keys(Keys.ENTER)
            break

    ##########시간 선택(minute)
    select_element = driver.find_element(By.XPATH, '//*[@id="info.subway.searchBox.minuteBox"]')
    select_element.send_keys(Keys.ENTER)
            
    minutes = driver.find_elements(By.CSS_SELECTOR, '#info\.subway\.searchBox\.listBox > li')
    for minute in minutes:
        title = minute.find_element(By.CSS_SELECTOR, 'a')
        title2 = title.get_attribute('innerText')
        #print(title2)
        if title2 == m:
            title.send_keys(Keys.ENTER)
            break

    ##########검색
    driver.find_element(By.XPATH, '//*[@id="info.subway.searchBox.submit"]').send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="info.subwayInfo"]/div/ul/li[1]/div[1]/a').send_keys(Keys.ENTER)
    
    ##########사진 출력 
    element = driver.find_element(By.XPATH, '//*[@id="view.subway.route"]')
    element_png = element.screenshot_as_png
    with open('route.png', "wb") as file:
        file.write(element_png)

    ##########역 출력
    st_list = []
    
    stations = driver.find_elements(By.CSS_SELECTOR, '#info\.subwayInfo > div > ul > li > div.detailView > ul > li')
    for station in stations:
        x = station.find_element(By.CSS_SELECTOR, 'div > div > span.name > a')
        y = station.find_element(By.CSS_SELECTOR, 'div > div > span.time')
        line = station.find_element(By.CSS_SELECTOR, 'div > div > p.direction')
        st_list.append([x.get_attribute('innerText'),y.get_attribute('innerText'),line.get_attribute('innerText')])
        sts = station.find_elements(By.CSS_SELECTOR, 'div > div > ul > li')
        for st in sts:
            title = st.find_element(By.CSS_SELECTOR, 'span.name')
            time = st.find_element(By.CSS_SELECTOR, 'span.time')
            st_list.append([title.get_attribute('innerText'),time.get_attribute('innerText'),line.get_attribute('innerText')])
    
    l_time = driver.find_element(By.CSS_SELECTOR, '#info\.subwayInfo > div > ul > li > div.detailView > p.detailStartEndNode.boldBottom > span.time')
    st_list.append([st2[:-1],l_time.get_attribute('innerText'),line.get_attribute('innerText')])
    
    ##########총 소요시간
    LTT = driver.find_element(By.XPATH, '//*[@id="info.subwayInfo"]/div/ul/li[1]/div[1]/p[1]').get_attribute('innerText')
    
    if LTT.count('시간')==2:
        LTh=LTT.split('시간')[0]
        LTm=LTT.split('시간')[1].split('분')[0].replace(' ','')
        LT=f'{LTh}시간 {LTm}분'
    else:
        LT=LTT.split('분')[0]+'분'
    
    return st_list, LT