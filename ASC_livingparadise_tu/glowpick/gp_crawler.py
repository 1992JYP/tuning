from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from datetime import datetime,timedelta
from time import sleep
import pandas as pd
import requests
import random as rd
import os
from fake_useragent import UserAgent 
from urllib import parse
import re
from datetime import datetime
import chromedriver_autoinstaller
from .models import CategoriCmk,CmkCtest,CmkCrtest,CmkBtest,CmkBrtest
from django.db.models import Q






class GlowPick_Crawler:
    def __init__(self):
        self.today = datetime.now()
        self.yesterday = self.today- timedelta(1)
        self.today = self.today.strftime("%Y-%m-%d")
        self.yesterday = self.yesterday.strftime("%Y-%m-%d")
        self.categori_base_url = 'https://www.glowpick.com/categories/'
        self.brandnew_base_url = 'https://www.glowpick.com/products/brand-new?cate1Id={}&cate2Id={}'
        self.item_review_list = []
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
        self.dpath = f'./{chrome_ver}/chromedriver.exe'
        options = wd.ChromeOptions()  #옵션 선언
        options.add_argument('headless')  #백그라운드 실행옵션
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        try:
            driver = wd.Chrome(self.dpath,options=options)  
            driver.quit() 
        except:
            chromedriver_autoinstaller.install(True)
            
        self.review_cqs = CmkCrtest.objects.all()   #카테고리리뷰
        self.review_bqs = CmkBrtest.objects.all()   #신제품리뷰

        self.regis_bqs = CmkBtest.objects.all()
        self.regis_cqs = CmkCtest.objects.all()
    
        
    def start(self, search_type):
        if search_type != 'categori' and search_type != 'brandnew':
            argument_error = 'argument_error: You must enter one of two values: category or brandnew'
            return print(argument_error)
        if search_type == 'categori':
            search_list = []
            search_list = self.categori_listup()
            self.item_product_list = []
            for cmk in tqdm(search_list, position=0, desc='카테고리 상품및 리뷰검색'):
                cid_list = []
                cidlist = cmk[2]
                for c in cidlist:
                    cid = c[c.find('-')+1:]
                    cid_list.append(cid)
                for cid in cid_list:
                    url = self.categori_base_url+cid  # 카테고리별 오픈 
                    driver,pageState = self.driveropen(url) # 오픈함수
                    self.item_search(driver,url,search_type,cmk)
                    driver.quit()
            self.csv_save(search_type)
        else:  #brandNew
            self.item_product_list = []
            search_list = []
            search_list = self.categori_listup()
            for cmk in tqdm(search_list, position=0, desc='브랜드뉴 상품및 리뷰검색'):
                cid_list = []
                cidlist = cmk[2]
                for c in cidlist:
                    cate1 = c[0:c.find('-')]
                    cate2 = c[c.find('-')+1:]
                    cid_list.append([cate1,cate2])
                for cli in cid_list:
                    url = self.brandnew_base_url.format(cli[0],cli[1])  # 카테고리별 오픈 
                    driver,pageState = self.driveropen(url) # 오픈함수
                    if pageState == 'No':
                        print('해당카테고리에 신제품이 존재하지않습니다.')
                        driver.quit()
                        continue
                    self.item_search(driver,url,search_type,cmk)
                    driver.quit()
                self.csv_save(search_type)
                
    #검색 리스트 뽑기 
    def categori_listup(self):
        qs = CategoriCmk.objects.all()
        qs = qs.filter(~Q(glowpick_cids=''))
        gp_list = []
        search_list = []
        
        
        for q in qs.values_list():
            gp_list.append(q)
        
        
        for li in gp_list:
            cid_list = []
            cmk_id = li[0]
            class_name = li[8]
            cid_list = li[9].split(',')
            search_list.append([cmk_id,class_name,cid_list])

        return search_list


            
    # 드라이버 오픈
    def driveropen(self,url):
        options = wd.ChromeOptions()  #옵션 선언
        # options.add_argument('headless')  #백그라운드 실행옵션
        # options.add_argument('window-size=1920x1080')  #백그라운드 실행옵션
        options.add_argument("disable-gpu")
        driver = wd.Chrome(self.dpath,options=options)
        driver.maximize_window() #화면에맞+춤   #창띄울때 사용 q백그라운드시 주석처리
        
        driver.implicitly_wait(time_to_wait=5)
        driver.get(url)
        sleep(1)
#         popup = driver.find_element_by_class_name('popup__container')
#         print(popup)
        self.Remove_Ads(driver) # 오픈시 광고 제거 

        this_url = driver.current_url
        if url != this_url:
            pageState = 'No'
        else:
            pageState = 'yes'

        return driver,pageState
    
    def Remove_Ads(self,driver):  #오픈시 광고 제거 
        try:
            try:
                driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/span/div[2]/div/div[6]/button/span').click()
            except:
                pass
            try:
                btn1 = driver.find_element_by_class_name('buttons__not-today').click() #광고제거
            except:
                sleep(0.5)
        except:
            print('광고 제거 실패')


    # 아이템페이지 검색 및 리뷰검색 
    def item_search(self,driver,url,search_type,cmk):
        itemnum = 1        
        try:
            ad = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[2]/ul/li[1]/div/div/div[1]/div/div[1]/span')
            self.ad = True
        except:
            self.ad = False

        if search_type == 'categori':
            gp_class = driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div/div/div[1]/div/h1/span[1]').text 
            print(gp_class)
        else:
            gp_class = driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div/div/div[3]/div/div[1]/div/span[1]').text
            print(gp_class)
        
        search_html = driver.page_source
        soup = bs(search_html, features="lxml")
        sleep(0.5)
        try:
            if search_type == 'categori':
                lastitemnum = soup.select('ul.ranking__list li')
                lastitemnum = len(lastitemnum)+1
            else:
                lastitemnum = soup.select('ul.new__wrapper__list li')
                if self.ad == True :
                    lastitemnum = len(lastitemnum)-1
                else:
                    lastitemnum = len(lastitemnum)

        except:  # 상품이 존재하지 않을시 해당페이지 보여준뒤 다음으로 넘어감
            error = '==상풍정보 없음=='+'\n'+'페이지URL = '+search_html
            return print(error)


        cktitle_list = self.item_title_ck_list(driver,search_type,soup)

        for itemnum in range(itemnum,lastitemnum):
            product = []
            #아이템 클릭해 들어감
            select_state = self.item_select(driver,itemnum,search_type,lastitemnum,cktitle_list)
            if select_state == 'error':
                continue
            this_url = driver.current_url
            #page 이동확인
            while url == this_url:
                print('url 이동체크')
                sleep(1)
                this_url = driver.current_url
            #상품 id 
            productId = this_url[34:]    
            soup,title = self.item_info(driver,itemnum,productId,gp_class,cmk,search_type,this_url)
            #리뷰
            self.duplicate_check_list = []
            sort_state = 'latest_ranking'
            self.review_search(soup,productId,title,cmk,search_type,sort_state)
            soup=self.review_sort(driver)
            sort_state = 'Popularity_Ranking'
            self.review_search(soup,productId,title,cmk,search_type,sort_state)
            
            driver.back() 
            sleep(2)
            
            
            
    # 리뷰좋아요많은순정렬    
    def review_sort(self,driver):
        sort_button = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section/section/div[3]/div/button')
        ActionChains(driver).move_to_element(sort_button).perform()
        
        sort_button.send_keys(Keys.ENTER)
        sleep(0.5)
        like_button = driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/span/div/div[2]/div/ul/li[2]/span')
        sleep(0.5)
        like_button.click()
        sleep(1)
        search_html = driver.page_source
        soup = bs(search_html, features="lxml")
        sleep(1)
        return soup
    
    #제대로된 아이템정보인지 체크 순서에 사용할 타이틀리스트 
    def item_title_ck_list(self,driver,search_type,soup):
        title_list = soup.select('div.product__details p.details__product span')
        cktitle_list = []
        for title in title_list:
            cht = title.get_text().replace('\n','').replace(' ','')
            cktitle_list.append(cht)
        return cktitle_list




        #아이템 클릭
    def item_select(self,driver,itemnum,search_type,lastitemnum,cktitle_list):
        lastitemnum = lastitemnum-1
        itemnum_dumy = itemnum     # 실패시 증가 방지 
        # print(self.ad)
        sleep(0.5)
        error_check = 'pass'
        itemSelectCount = 0
        while True:
            if error_check == 'error':
                itemnum = itemnum_dumy                                  
            try:                                     
                if search_type =='categori':            
                    item = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/ul/li['+str(itemnum)+']')
                else:
                    if self.ad == True:
                        if itemnum >= 5:
                            itemnum = itemnum+1
                        item = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div/ul/li['+str(itemnum+1)+']')
                        print(itemnum)
                    else:
                        if itemnum >= 6:
                            itemnum = itemnum+1
                        item = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div/ul/li['+str(itemnum)+']')

                ActionChains(driver).move_to_element(item).perform()
               

                item.click()
                
                    
                sleep(1)
                item_check = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section/div[2]/p[2]').text.replace('\n','').replace(' ','')
                if self.ad == True:
                    print(cktitle_list[itemnum_dumy],'     ',item_check)
                    if cktitle_list[itemnum_dumy] != item_check:
                        error_check = 'error'
                        driver.back()
                        sleep(3)
                        continue
                break
            except:                                       
                if search_type =='categori':             
                    try:
                        move = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/ul/li['+str(lastitemnum)+']')
                        ActionChains(driver).move_to_element(move).perform()
                    except:
                        print('마지막제품이동')
                        driver.refresh()
                        sleep(3)
                        pass
                else:
                    try:
                        move = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div/ul/li['+str(lastitemnum-1)+']')
                        ActionChains(driver).move_to_element(move).perform()
                    except:
                        print('마지막제품이동')
                        driver.refresh()
                        sleep(3)
                        pass
                print('아이템선택중')
                itemSelectCount = itemSelectCount +1 
                if itemSelectCount == 3:
                    error_check = 'error'
                    return error_check
                driver.refresh()
                sleep(1)
        sleep(2)
        
        return error_check
        # print('아이템 선택완료================ 상세검색시작')

    #상세 페이지 닫기
    def detail_page_exit(self, driver):
        while True:
            try:
                exit = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/span/div/div[2]/h1/button').click()
                break
            except:
                print('상세페이지닫기')
                sleep(1)
                
                
                
        # 상품검색        
    def item_info(self,driver,itemnum,productId,gp_class,cmk,search_type,this_url):
        search_html = driver.page_source
        soup = bs(search_html, features="lxml")
        sleep(1)
        #제품 구성 및 설명 리스트
        lilist = soup.select('div.product__info article')
        ingredient_num = 11
        detail_num = 11
        for li in range(1,len(lilist)+1):                      
            try:
                text = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/section/div[3]/article['+str(li)+']/h3').text
            except:                                  
                text = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section/div[3]/article['+str(li)+']/h3').text
            if text.find('성분 구성') != -1:
                ingredient_num = li
            elif text.find('제품 설명') != -1:
                detail_num = li
            
        #성분 상세 페이지 클릭  
        error_count = 0  
        while True:
            try:          
                # ingclick = driver.find_element_by_class_name('info__article__h3__button').click()
                ingclick = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section/div[3]/article['+str(ingredient_num)+']/h3/button').click()
                break
            except:
                error_count = error_count + 1
                print('성분상세페이지클릭')
                self.Remove_Ads(driver) # 오픈시 광고 제거
                try:
                    check = driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div/footer/div/aside/div')
                    if check:
                        move = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section/section/div[2]/div[1]/input')
                        print('scrol move')
                        ActionChains(driver).move_to_element(move).perform()

                except:
                    pass    
                sleep(1)
                
        sleep(0.5)
        search_html = driver.page_source
        soup = bs(search_html, features="lxml")
        if ingredient_num != 11:
            #성분구성
            ingredient_list = soup.select('ul.ingredient__list li')
            ingredientlist = ''
            for ditem in ingredient_list:
                ingredient = ditem.select_one('p.item__wrapper__text__kor').get_text().replace(' ','')
                # try:
                #     danger = ditem.select_one('p.tag__label').get_text().replace(' ','')
                # except:
                #     danger = '0'
                ingredient = ingredient+','          #danger+
                ingredientlist = ingredientlist+ingredient
            sleep(0.5)    
            #성분구성상세창 끄기     
            self.detail_page_exit(driver)
        else:
            ingredientlist = ''

        if detail_num != 11:
                
            #제품 상세 
            
            while True:
                try:                                            
                    detailclick = driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/section/div[3]/article['+str(detail_num)+']/h3/button').click()
                    break
                except:
                    print('제품상세페이지클릭')
                    sleep(1)
            sleep(0.5)
            search_html = driver.page_source
            soup = bs(search_html, features="lxml")
            #상세설명
            detail_data = soup.select_one('div.descriptions article pre.descriptions__article__pre')
            detail = detail_data.get_text().replace('\n','')
             #상세페이지 종료
            self.detail_page_exit(driver)
        else:
            detail = ''
        title_price_data = soup.select_one('span.offer__volume-price').get_text().replace(' ','') #용량과 가격을 가지고있는데이터
        title_price_data = title_price_data.replace('\n','')
        slush = title_price_data.find('/')  # 용량과 가격사이 슬러시 위치 
        amount = title_price_data[:slush]  #용량
        price = title_price_data[slush+1:].replace(',','')
        price = price.replace('원','')
        title = soup.select_one('p.product__summary__name').get_text().replace('\n','').replace(' ','')
        title = title + amount
        grade = soup.select_one('span.stars__rating').get_text()
        imgpath = soup.select('img.image__img')
        for img in imgpath:
            ick = img.get('alt').replace('\n','').replace(' ','')
            if ick == '제품이미지':
                imgpath = img.get('src')
#         imgpath = imgpath[1].get('src')
        ranking = itemnum
        try:
            review_count = soup.select_one('span.reviews__header__count').get_text()
        except:
            review_count = '0'
        try:
            brand = soup.select_one('button.product__summary__brand__name').get_text().replace(' ','')
            brand = brand.replace('\n','')
        except:
            brand = ''
        cmk_id = cmk[0]
        second_class_name = cmk[1]
        date_info = self.today
        
        
        #제품등록일 설정
        regis_check_list = []
        if search_type == 'categori':
            regis_check_list = self.regis_cqs.filter(cmk_id__icontains=cmk_id,second_class_name__icontains=second_class_name,gp_class__icontains=gp_class,productid__icontains=productId).order_by('date_info') 
        else:
            regis_check_list = self.regis_bqs.filter(cmk_id__icontains=cmk_id,second_class_name__icontains=second_class_name,gp_class__icontains=gp_class,productid__icontains=productId).order_by('date_info') 


        if regis_check_list:
            # print('data true')
            registration_date = regis_check_list.values_list()
            registration_date = registration_date[0][15]
        else:
            # print('data false')
            registration_date = date_info

        product = [cmk_id,second_class_name,gp_class,productId,title,ranking,price,grade,review_count,brand,ingredientlist,detail,this_url,imgpath,date_info,registration_date]

        self.item_product_list.append(product)
        self.item_db_save(search_type,product)
       
        
        
        return soup,title
    
    def item_db_save(self,search_type,product):
        if search_type == 'categori':
            CmkCtest(cmk_id = product[0],second_class_name = product[1],gp_class = product[2],productid = product[3],title = product[4], ranking = product[5],
            price = product[6],grade = product[7], review_count = product[8], brand = product[9],ingredientlist = product[10],detail = product[11],
            url = product[12],imgpath = product[13],date_info = product[14],registration_date = product[15]).save()
        else:
            CmkBtest(cmk_id = product[0],second_class_name = product[1],gp_class = product[2],productid = product[3],title = product[4], ranking = product[5],
            price = product[6],grade = product[7], review_count = product[8], brand = product[9],ingredientlist = product[10],detail = product[11],
            url = product[12],imgpath = product[13],date_info = product[14],registration_date = product[15]).save()


    #리뷰작성일 계산 
    def review_date_change(self,date):
        today = datetime.now()
        if date.find('시간전') != -1:
            review_create_date = self.today
        elif date.find('일전') != -1:
            minusDay = int(date.replace('일전',''))
            review_create_date = today - timedelta(minusDay)
            review_create_date = review_create_date.strftime('%Y-%m-%d')
            
        elif date.find('개월전') != -1:
            minusDay = int(date.replace('개월전',''))*30
            review_create_date = today - timedelta(minusDay)
            review_create_date = review_create_date.strftime('%Y-%m-%d')
            #뒷자리 01로통일
            review_create_date = review_create_date[:8] + '01'
        else:
            review_create_date = date
        return review_create_date
            
    
        # 리뷰검색
    def review_search(self,soup,productId,title,cmk,search_type,sort_state):
        review_list = soup.select('div.reviews__wrapper article')
        cmk_id = cmk[0]
        dupli_state = False
        for review in review_list:
            content = []
            review_check = []
            user_name = review.select_one('p.info__details__nickname').get_text()
            userdata = review.select('span.property__wrapper__item')
            user_age = userdata[0].get_text().replace(' ','')
            user_age = user_age.replace('\n','').replace('세','')
            user_type = userdata[1].get_text().replace(' ','').replace('\n','')
            user_gender= userdata[2].get_text().replace(' ','').replace('\n','')
            user_star = review.select_one('span.stars__rating').get_text().replace(' ','').replace('\n','')
            #작성일 
            date = review.select_one('span.review__side-info__created-at').get_text().replace(' ','').replace('\n','')
            review_create_date = self.review_date_change(date)
            review_content = review.select_one('pre.cutter__pre').get_text().replace('\n','').replace(',','')
            review_content=review_content.replace("[^0-9 가-힣 a-z A-Z ]", "")

            
            if search_type == 'categori':
                if sort_state =='latest_ranking':  #최신순일경우 중복된 리뷰가 그전데이터는 이미 있는데이터 이므로 다음상품으로 넘어감
                    review_check = self.review_cqs.filter(cmk_id__icontains=cmk_id,productid__icontains=productId,user_name__icontains=user_name,review_create_date__icontains=review_create_date,
                    review_content__icontains=review_content)
                    if review_check:
                        break
                    else:
                        pass
                else:   #인기순일경우 중복된리뷰면 저장안하고 다음것 확인 인기순은 순위의 변동이있을수있기때문 
                    review_check = self.review_cqs.filter(cmk_id__icontains=cmk_id,productid__icontains=productId,user_name__icontains=user_name,review_create_date__icontains=review_create_date,
                    review_content__icontains=review_content)
                    if review_check:
                        continue
                    else:
                        pass
            else: #
                if sort_state =='latest_ranking':  #최신순일경우 중복된 리뷰가 그전데이터는 이미 있는데이터 이므로 다음상품으로 넘어감
                    review_check = self.review_bqs.filter(cmk_id__icontains=cmk_id,productid__icontains=productId,user_name__icontains=user_name,review_create_date__icontains=review_create_date,
                    review_content__icontains=review_content)
                    if review_check:
                        break
                    else:
                        pass
                else:   #인기순일경우 중복된리뷰면 저장안하고 다음것 확인 인기순은 순위의 변동이있을수있기때문 
                    review_check = self.review_bqs.filter(cmk_id__icontains=cmk_id,productid__icontains=productId,user_name__icontains=user_name,review_create_date__icontains=review_create_date,
                    review_content__icontains=review_content)
                    if review_check:
                        continue
                    else:
                        pass     
                




            content = [cmk_id,productId,title,user_name, user_age,user_type,user_gender,user_star,review_create_date,review_content]
            
            # 리뷰 중복 체크 
            # 해당 아이템 리뷰중 중복체크  인기순, 최신순
            for dupli in self.duplicate_check_list:
                dupli_state = dupli==content
                if dupli_state:
                    break
            if dupli_state == False:
                self.duplicate_check_list.append(content)
                self.item_review_list.append(content)   
                self.review_db_save(content,search_type)
            else:
                pass
    
    def review_db_save(self,content,search_type):
        if search_type == 'categori':
            CmkCrtest(cmk_id = content[0],productid = content[1],title = content[2],user_name = content[3],user_age = content[4],user_type = content[5],
            user_gender = content[6],user_star = content[7],review_create_date = content[8],review_content = content[9]).save()
        else:
            CmkBrtest(cmk_id = content[0],productid = content[1],title = content[2],user_name = content[3],user_age = content[4],user_type = content[5],
            user_gender = content[6],user_star = content[7],review_create_date = content[8],review_content = content[9]).save()


    
        # product = [cmk_id,second_class_name,gp_class,productId,title,ranking,price,grade,review_count,brand,ingredientlist,detail,imgpath]
        # content = [gp_class,productId,title,user_name, user_age,user_type,user_gender,user_star,review_create_date,review_content]
    
            
        #csv 파일 저장 
    def csv_save(self,search_type):
        #상품저장
        filename = 'GlowPick_{}_Product_{}.csv'.format(search_type,self.today)
        filepath ='C:/Croling/cosmeca/glowpick/'+ filename
    
        try:
            df = pd.DataFrame(self.item_product_list, columns=['CMKID','SECOND_CLASS','GLOWPICK_CALSS','PRODUCT_ID','TITLE','RANKING','PRICE','GRADE','REVIEW_COUNT',
            'BRAND','INGREDIENTLIST','DETAIL','URL','IMGPATH','DATE_INFO','REGOSTRATION_DATE'])
            df.to_csv(filepath, index=False, encoding='utf-8') 
        except:
            print('item_save_error')
            
        
        
        
        
        #리뷰저장
        filename = 'GlowPick_{}_Review_{}.csv'.format(search_type,self.today)
        filepath ='C:/Croling/cosmeca/glowpick/'+ filename
        
        
        try:
            df = pd.DataFrame(self.item_review_list, columns=['CMK_ID','PRODUCT_ID','TITLE','USER_NAME','USER_AGE','USER_TYPE','USER_GENDER','USER_STAR','REVIEW_CREATE_DATE','REVIEW_CONTENT'])
            df.to_csv(filepath, index=False, encoding='utf-8') 
        except:
            print('review_save_error')
