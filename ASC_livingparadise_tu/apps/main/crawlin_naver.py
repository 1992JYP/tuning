from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import tqdm_notebook
from selenium.webdriver.common.alert import Alert
#======================================================================================================

url = 'https://shopping.naver.com/'
options = wb.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")

 

driver = wb.Chrome('chromedriver', chrome_options=options)
#driver = wb.Chrome()
driver.get(url)


# 검색 창 찾기 - 네이버 기준
elem = driver.find_element_by_name("query")
# 제품명 변수 지정
pd_name = '생활낙원'
# 찾은 검색 창에 검색 
elem.send_keys(pd_name)
time.sleep(1)
# 엔터 
elem.send_keys(Keys.RETURN)
time.sleep(3)
#======================================================================================================

review_list = [] # 리뷰담을 리스트

page = 10  ## 크로링 네이버 페이지 수
count =1 # 개수 파악용 인덱스
total =100 # 크롤링 상품 페이지 수
next_num = 2 # 제품 페이지 다읽고 넘기는 태그번호
cnt = 0
#======================================================================================================

reviewDF = pd.DataFrame(columns=['index', 'serial_number', 'text', 'score', 'option','review_date'])
productDF = pd.DataFrame(columns=['index', 'keyword', 'title', 'price', 'review_count', 'reg_date', 'seller_name', 'iis_ad', 'serial_number', 'prod', 'link', 'score_avg', 'image'])
#======================================================================================================

def smartstore():
    global reviewDF
    global smart_infor1
    
    try:
        re_count = int(driver.find_element_by_css_selector('#content > div > div._2-I30XS1lA > div._25tOXGEYJa > div.NFNlCQC2mv > div:nth-child(1) > a > strong').text.replace(',',''))
        re_next_num = 3 # 리뷰 다음페이지 태그 번호
        review_tag = 1
        # range안에 원하는 갯수 적어 넣고 돌다가 그 페이지가 갖고있는 리뷰 갯수가 원하는 갯수보다 작으면 딱 거까지만 뽑아놓고 빠져나온다 오류 안남
        
        serial_number = driver.find_element_by_css_selector('#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(1) > td:nth-child(2) > b').text
        print('serial_number 긁음 : {}'.format(serial_number)) # 상품번호 클릭후 안에서 밖에서필요 고정
        
        prod = driver.find_element_by_css_selector('#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
        print('prod도 긁음') # 제조사 클릭후 안에서 밖에서필요 고정

        score_avg  = driver.find_element_by_css_selector('#REVIEW > div > div._25tRcZzaD2 > div:nth-child(1) > div > div > div.TFNhvMOrjC._3uz9pzdFUe > div > span').text.replace('총','').replace('5','').replace('점 중','').replace('점','')
        print('score_avg 긁음') # 밖에서필요 고정

        image = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img').get_attribute('src')
        print('image도 긁음') # 상품이미지경로 클릭후 안에서 밖에서필요 고정

        ## 해당 url 주소 가져오기  밖에서필요 고정
        link = driver.current_url
        print('현url도 긁음')
            
        smart_infor1 = [serial_number, prod, link, score_avg, image]
        if re_count > 2000:
            re_count = 2000
        for index in tqdm_notebook(range(re_count)):   

            print(index)
            review_list.append(driver.find_element_by_css_selector('ul > li:nth-child(%d) > div > div'%review_tag))
            #review_list.append(driver.find_element_by_xpath('//*[@id="REVIEW"]/div/div[3]/div/div[2]/ul/li[%d]/div/div/a'%review_tag)
            time.sleep(1)
            review_list[index-1].click
            time.sleep(1)
            
            text = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul > li:nth-child(%d) > div > div._30o7PGmsIy > div > div._1XNnRviOK8 > div > div > div._19SE1Dnqkf > div > span._3QDEeS6NLn'%review_tag).text 
            print('{} 번째 text 긁음'.format(index +1)) # 리뷰텍스트 클릭후 안에서 a
            
            score = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul > li:nth-child(%d) > div > div > div > div._1XNnRviOK8 > div > div > div._1rZLm75kLm > div._37TlmH3OaI > div._2V6vMO_iLm > em'%review_tag).text
            print('score 긁음') # 리뷰점수 클릭후 안에서a

            review_date = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul > li:nth-child(%d) > div > div > div > div._1XNnRviOK8 > div > div._1YShY6EQ56 > div._1rZLm75kLm > div._37TlmH3OaI > div._2FmJXrTVEX > span'%review_tag).text
            print('review_date 긁음') # 리뷰등록날자 클릭후 안에서a
            

            option = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul > li:nth-child(%d) > div > div > div > div._1XNnRviOK8 > div > div._1YShY6EQ56 > div._1rZLm75kLm > div._37TlmH3OaI > div._14FigHP3K8 > div > button > span'%review_tag).text
            print('option 긁음') # 제품디자인 클릭후 안에서a
            
            reviewDF.loc[len(reviewDF)]=[index+1,serial_number, text, score, option, review_date ]
    
            print('{} 번째 까지 다 긁음===================================='.format(index +1))
        
            
            if review_tag >= 20:
                if re_next_num > 11:
                    print('re_next_num이 11보다 큰 {}이네요'.format(re_next_num))
                    driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a:nth-child(%d)'%re_next_num).send_keys(Keys.ENTER)
                    re_next_num = 2
                    time.sleep(1)
                else:
                    driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a:nth-child(%d)'%re_next_num).send_keys(Keys.ENTER)
                    re_next_num += 1
                    review_tag = 1
            else:
                review_tag += 1
                
            time.sleep(2)
        return smart_infor1    
    
    except:
        print('smart리뷰수없음')
        pass
    return smart_infor1


def naverallitems(i):
    print('상품정보긁는중. . .')
    title = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a'%i).text
    print('title 긁음')

    price = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_price_area__1UXXR > strong > span > span.price_num__2WUXn'%i).text
    print('price 긁음')
    
    try:
        review_count = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_etc_box__1Jzg6 > a:nth-child(1) > em'%i).text
        print('review_count 긁음')
    except:
        review_count = 'null'
        print('review_count 긁음')
        
    try:    
        seller_name = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_mall_area__lIA7R > div.basicList_mall_title__3MWFY > a.basicList_mall__sbVax'%i).text
        print('seller_name 긁음')
    except:
        seller_name = 'null'
        print('seller_name가 안들어있음')
        
    reg_date = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[%d]/li/div/div[2]/div[5]/span[1]'%i).text.replace('등록일','')
    print('reg_date 긁음')
     
    try:
        iis_ad = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_price_area__1UXXR > button'%i).text
        print('iis_ad 긁음')
    except:
        iis_ad = 'null'
        print('iis_ad 안들어있음')
          
    print('=========상품정보 긁어 담음============')
          
    naveritme_infor2 = [title, price, review_count, reg_date, seller_name, iis_ad]
          
    return naveritme_infor2
#======================================================================================================

for i in range(5):
    driver.execute_script("window.scrollTo(0, 9000)")
    time.sleep(1)

for i in range(1,total+1):
    title_url = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a'%i) 
    ## 선택한 제품 클릭 
    title_url.send_keys(Keys.RETURN)
    time.sleep(4)

    ## 제품 선택하고 생성된 새창으로 포커스 이동 
    last_tab = driver.window_handles[-1]
    driver.switch_to.window(window_name = last_tab)
    time.sleep(3)

    ## 해당 url 주소 가져오기 
    input_url = driver.current_url

    ## 가져온 주소에서 smartstore.naver.com 있는지 판단  -1 이 있다면 없음 
    naver_shop = input_url.find('smartstore.naver.com') #  주소안에스마트스토어만 찾아서 담아
        
#===============================================================================        

        ## 불러온 url  -1 이면 
    if naver_shop == -1:
        # 해당 창 닫기 
        #print(False)

        naver_shop = input_url.find('search.shopping.naver.com')

        if naver_shop == -1:
            c_type = -1
            #driver.close()

        else :
            c_type = 2

    else :
        c_type = 1
            
#===============================================================================


        # 여긴 조건을 봐서 바로 꼿아버리는데
    if c_type == 1:  # smartstore.naver.com 스마트스토어라면 여기로 들어가 (크롤링완성)

        smart_search_infor1 = smartstore()

        driver.close()
        last_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=last_tab)

        # 먼저 긁어와서 담아봐
        smart_items_infor = naverallitems(i)

        next_num += 1
        re_next_num = 3
        review_tag = 1
        cnt += 1

        insertlist = [i,pd_name ]+smart_items_infor + smart_search_infor1
        productDF.loc[len(productDF)] = insertlist

    elif c_type == 2: # search.shopping.naver.com 이라면 여기로 들어가 (크롤링 만들어야함)

#        naver_search_infor = searchshop()

        driver.close()
        last_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=last_tab)

        # 먼저 긁어와서 담아봐
#        naver_items_infor = naverallitems(i)

#        next_num += 1
#        re_next_num = 3
#        review_tag = 1
#        cnt += 1

#        insertlist = [i,pd_name ]+naver_items_infor + naver_search_infor
#        productDF.loc[len(productDF)] = insertlist

    else:
        driver.close()
        last_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=last_tab)
        # 팝업 창 닫기 
        if len(driver.window_handles) >2:
            last_tab = driver.window_handles[1]
            driver.switch_to.window(window_name=last_tab)
            driver.close()

    if i >= 47:
        driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.pagination_pagination__6AcG4 > div > a:nth-child(%d)'%next_num).send_keys(Keys.ENTER)
        i = 1
        next_num += 1
        if next_num >= 11:
            driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.pagination_pagination__6AcG4 > a').send_keys(Keys.ENTER)

    if cnt == 10:
        break

driver.quit()
