from numpy import product
from numpy.lib.function_base import average
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

from crawling.views import item_search
from .models import NvProduct,NvReview
from apps.paradise.models import ProductMaster

from django.db.models import Q

import multiprocessing






class naver_Crawler:
    def __init__(self):
        self.today = datetime.now()
        self.yesterday = self.today- timedelta(1)
        self.today = self.today.strftime("%Y-%m-%d")
        self.yesterday = self.yesterday.strftime("%Y-%m-%d")
        self.excelfile_name = '매칭키워드_정리_URL 매칭.xlsx'
        self.excelsheet_name = 'Sheet1'
        self.item_review_list = []
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
        self.dpath = f'./{chrome_ver}/chromedriver.exe'
        options = wd.ChromeOptions()  #옵션 선언
        options.add_argument('headless')  #백그라운드 실행옵션
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        self.save_path = 'C:/Croling/living_paradise/Naver/' ####### 본인 폴더에 맞게 수정필요
        if not os.path.isdir(self.save_path) :
            os.mkdir(self.save_path)
        try:
            driver = wd.Chrome(self.dpath,options=options)  
            driver.quit() 
        except:
            chromedriver_autoinstaller.install(True)
        self.naver_base_url = 'https://search.shopping.naver.com/search/all?pagingIndex={}&query={}'           
        self.ssUrl= 'https://search.shopping.naver.com/'
        self.smUrl= 'https://smartstore.naver.com/'
        self.smUrl1 = 'https://brand.naver.com/'
        self.smUrl2 = 'https://shopping.naver.com/'

        

    def search_listup(self):
        try:
            item_list =[]
            # 자사 상품목록 가져오기 
            try:
                qs = ProductMaster.objects.all()
                for s in qs.values_list():
                    item_list.append(s)
                df = pd.DataFrame(item_list, columns=['ID','담당','품목코드','품목명','브랜드','매칭키워드','네이버코드','네이버URL','쿠팡코드','쿠팡URL','이미지'])
            except:
                # db접속안될시 excel 파일
                df = pd.read_excel(io='C:/Croling/living_paradise/'+self.excelfile_name, sheet_name=self.excelsheet_name)
                self.dbstate = 'faile'
            
            df = df.dropna(subset=['네이버URL','매칭키워드'])  #결측치 제거
            matchingKeyword = df['매칭키워드']
            matchingKeyword = matchingKeyword.drop_duplicates()  #중복제거
            keyword_lst=matchingKeyword.values.tolist()
            # 여러개 행을 선택할때 loc 사용
            url_list = df.loc[:,['품목코드','네이버URL']]
            url_list = url_list.values.tolist()
            # self.df = df.values.tolist()
            # print(self.df)
            # url_list = df.values.tolist()
            #검색 키워드 리스트 뽑기
            
                
        except:
            print('상품정보를 가져오는데 실패 하였습니다.')
            keyword_lst = ['']
        return keyword_lst, url_list



    def driveropen(self,url):
            options = wd.ChromeOptions()  #옵션 선언
            # options.add_argument('headless')  #백그라운드 실행옵션
            # options.add_argument('window-size=1920x1080')  #백그라운드 실행옵션
            options.add_argument("disable-gpu")
            driver = wd.Chrome(self.dpath,options=options)
            driver.maximize_window() #화면에맞+춤   #창띄울때 사용 q백그라운드시 주석처리
            
            driver.implicitly_wait(time_to_wait=5)
            driver.get(url)
            sleep(0.8)
            # this_url = driver.current_url

            return driver          

    def header(self):
        ua = UserAgent()    
        headers = {
            'User-Agent' : ua.random,    
        }
        return headers



    def last_page(self,url):
        headers = self.header()
        print(url)
        res = requests.get(url, headers=headers)
        print(res.status_code,'----------------------------------------------------------------------------------')
        while res.status_code != 200:
            res = requests.get(url, headers=headers)
            sleep(2)
        if res.status_code == 200:
            soup = bs(res.text,features="lxml")
        try:
            all_item_count = soup.select_one('span.subFilter_num__2x0jq').get_text().replace(',','')    # 전체 상품개수
        except:
            sleep(3)
            print('전체상품개수 recome')
            res = requests.get(url, headers=headers)
            sleep(1)
            if res.status_code == 200:
                soup = bs(res.text,features="lxml")
                all_item_count = soup.select_one('span.subFilter_num__2x0jq').get_text().replace(',','')    # 전체 상품개수


        all_item_count = int(all_item_count)
        last_page = (all_item_count//40)+1
        return last_page
    
    
    
    def scroll_down(self,driver):
        sleep(1)
        for i in range(5):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(0.3)
        sleep(1)
    
    def productid(self, link):
        start = link.find('nvMid=')+6
        end = link.find('&catId=')
        productid = link[start:end]
        return productid


    def sold_out_check(self, link,driver):
        #품절체크
        state = ''
        ssUrl_check = link.startswith(self.ssUrl)
        smUrl_check = link.startswith(self.smUrl)
        smUrl_check1 = link.startswith(self.smUrl1)
        smUrl_check2 = link.startswith(self.smUrl2)
        if ssUrl_check:
            try:
                soldout_check = driver.find_element_by_xpath('/html/body/div/div/div[2]/h2')
                state = soldout_check.text
            except:
                state = '판매중'
        elif smUrl_check or smUrl_check1 or smUrl_check2: 
            state = '판매중'
        else:
            state = '판매중'

        return state


    def img_select(self,driver,i):
        try:
            try:
                try:
                    move = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[3]/div[1]/ul/div/div['+str(i)+']/li/div/div[1]/div/a')
                    ActionChains(driver).move_to_element(move).perform()
                    imgpath = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[3]/div[1]/ul/div/div['+str(i)+']/li/div/div[1]/div/a/img')
                    img = imgpath.get_attribute('src')
                except:
                    move = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div[1]/ul/div/div['+str(i)+']/li/div/div[1]/div/a')
                    ActionChains(driver).move_to_element(move).perform()
                    imgpath = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div[1]/ul/div/div['+str(i)+']/li/div/div[1]/div/a/img')
                    img = imgpath.get_attribute('src')
            except:                                     
                try:
                    move = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child('+str(i)+') > li > div > div.basicList_img_area__a3NRA > div > a')
                    ActionChains(driver).move_to_element(move).perform()
                    imgpath = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child('+str(i)+') > li > div > div.basicList_img_area__a3NRA > div > a > img')
                    img = imgpath.get_attribute('src')            
                except:
                    move = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child('+str(i)+') > li > div > div.basicList_img_area__a3NRA > div > a')
                    ActionChains(driver).move_to_element(move).perform()
                    imgpath = driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child('+str(i)+') > li > div > div.basicList_img_area__a3NRA > div > a > img')
                    img = imgpath.get_attribute('src')             
        except:
            img = 'none'                                                            
        return img





    def item_search(self,keyword_list,my_url_list):
        # keyword_list,my_url_list = self.search_listup()
        
        item_list = []
        for key in tqdm(keyword_list, position=0, desc='키워드상품검색'):
            tasa = 0
            jasa = 0
            itemMax = 100
            key = key.replace(' ','')
            url = self.naver_base_url.format('1',key)
            last_page = self.last_page(url)
            if last_page >3:
                last_page = 3
            nitem_c = 0
            ranking = 0
            ad_count = 4
            for item_page in range(1,last_page):
                
                if nitem_c==itemMax:
                    break
                url = self.naver_base_url.format(item_page,key)
                driver = self.driveropen(url)
                self.scroll_down(driver)
                html = driver.page_source
                soup = bs(html, features="lxml")
                sleep(1)
                item_search_list = soup.select('li.basicList_item__2XT81') 
                img_list = []
                print(url)
                ad_count = (ad_count * item_page)+2
                for i in tqdm(range(1,len(item_search_list)+1),position=0,desc='이미지검색'):
                        if image_count > itemMax+ad_count:
                            break
                        img = self.img_select(driver,i)
                        img_list.append(img)
                        image_count = image_count +1
                driver.quit()
               
                AD = 0
                Product = 0
                img_int = -1
                for item in tqdm(item_search_list,position=0,desc='page_itemsearch'):
                    if nitem_c==itemMax:
                        break
                    search = []
                    try:
                        adCheck = item.select_one('button.ad_ad_stk__12U34').get_text()
                    except:
                        adCheck = '상품'
                    if adCheck == '광고':
                        AD = AD+1
                        img_int = img_int+1
                        continue
                    else:
                        Product = Product+1    
                        img_int = img_int+1
                    review_count = int(item.select_one('em.basicList_num__1yXM9').get_text().replace(',',''))
                    #아이템선택
                    item_title = item.select_one('a.basicList_link__1MaTN')
                    link = item_title['href']
                    productid = self.productid(link)
                    title = item_title.get_text()
                    img = img_list[img_int]
                    # print(title,'====',img)
                    price = item.select_one('span.price_num__2WUXn').get_text().replace(',','').replace('원','')
                    try:
                        review_count = item.select_one('a.basicList_etc__2uAYO em.basicList_num__1yXM9').get_text()
                    except:
                        review_count = '0'
                    try:
                        brand = item.select_one('div.basicList_mall_title__3MWFY a.basicList_mall__sbVax').get_text()
                    except:
                        brand = ''
                    if brand == '쇼핑몰별 최저가':
                        brand = ''
                    try:
                        grade = item.select_one('span.basicList_star__3NkBn').get_text()
                        grade = grade.replace('별점','').replace(' ','')
                    except:
                        grade = '0'
                    registration_date = item.select_one('span.basicList_etc__2uAYO').get_text().replace('등록일','').replace(' ','')
                    keyword = key
                    driver = self.driveropen(link)
                    this_url = driver.current_url
                    link = this_url
                    state = self.sold_out_check(link,driver)
                    
                    if url.find('search.shopping.naver.com')!= -1:
                        html = driver.page_source
                        soup = bs(html, features="lxml")
                        sleep(0.5)
                        try:
                            manufacturer_list = soup.select('div.top_info_inner__1cEYE span.top_cell__3DnEV')
                            for mf in manufacturer_list:
                                manu = mf.get_text()
                                if manu.find('브랜드') != -1:
                                    brand = manu.replace('\n','').replace('브랜드','').replace(' ','')
                        except:
                            brand = ''
                    elif url.find('smartstore.naver.com') != -1:
                        try:
                            html = driver.page_source
                            soup = bs(html, features="lxml")
                            sleep(0.5)
                            manufacturer_list = soup.select_one('table._1_UiXWHt__ tbody')
                            name = manufacturer_list.select('tr th')
                            index = 0
                            brandindex = 0
                            for na in name:
                                if na.get_text().find('브랜드') != -1:
                                    brandindex = index
                                index = index+1           
                            result_list = manufacturer_list.select('tr td')
                            
                            if brandindex != 0:
                                brand = result_list[brandindex].get_text()
                            else:
                                brand = ''
                        except:
                            brand = ''
                    driver.quit()
                    sleep(1)
                    
                    
                    item_code = ''
                    for ckurl in  my_url_list:
                        if this_url == ckurl[1]:
                            item_code = ckurl[0]
                            company = '0'
                    if item_code == '':
                        company = '1'
                    ranking = ranking+1
                    date_info = self.today
                    search = [ranking,company,item_code,keyword,title,price,review_count,brand,link,productid,grade,img,state,date_info,registration_date] 
                    nitem_c = nitem_c+1
                    if company == '1' :    #타사제품
                        if tasa < 3:
                            NvProduct(ranking=ranking,company=company,item_code=item_code,keyword=keyword,title=title,price=price,
                            review_count=review_count,brand=brand,link=link,productid=productid,grade=grade,img=img,date_info=date_info,registration_date=registration_date).save()
                            item_list.append(search)
                        tasa = tasa + 1
                        
                        
                    else:
                        NvProduct(ranking=ranking,company=company,item_code=item_code,keyword=keyword,title=title,price=price,
                        review_count=review_count,brand=brand,link=link,productid=productid,grade=grade,img=img,date_info=date_info,registration_date=registration_date).save()
                        item_list.append(search)
                        jasa = jasa+1



        try:
            filename = 'naver_product_{}.csv'.format(self.today)
            filepath ='C:/Croling/cosmeca/naver/'+ filename                    
            df = pd.DataFrame(item_list, columns=['ranking','company','item_code','keyword','title','price','review_count','brand',
            'link','productid','grade','img','date_info','registration_date'])
            df.to_csv(filepath, index=False, encoding='utf-8') 
            print('csv save succes')  
        except:
            print('csv save error')
        

                    
        return item_list            
                    
                    
               
            


    
    def review_search(self):
        today = self.yesterday
        qs = NvProduct.objects.filter(date_info__icontains=today)
        search_list = qs.filter(company=0).values()
        allreview_list = []

        for item in search_list:
            print(item)
            m_review_list =[]
            s_review_list =[]
            url = item['link']
            title = item['title']
            item_code = item['item_code']
            review_count = item['review_count']
            productid = item['productid']
            ssUrl_check = url.startswith(self.ssUrl)
            smUrl_check = url.startswith(self.smUrl)
            smUrl_check1 = url.startswith(self.smUrl1)
            smUrl_check2 = url.startswith(self.smUrl2)
            if ssUrl_check:
                print('searchShoping')
                s_review_list = self.search_shopping(title,item_code,productid,review_count,url)
                if s_review_list:
                    allreview_list = allreview_list+s_review_list
            elif smUrl_check or smUrl_check1 or smUrl_check2:
                print('samrtShoping')
                m_review_list = self.smart_shopping(title,item_code,productid,review_count,url)
                if m_review_list:
                    allreview_list = allreview_list+m_review_list




        
                    

        df = pd.DataFrame(allreview_list, columns=['item_doce','productid','title','item_option','user_name','user_star','review_create_date','review_content'])
        filename = 'naver_review_{}.csv'.format(today)
        filepath =self.save_path+ filename 
        df.to_csv(filepath, index=False, encoding='utf-8')
        # 최신순/ 속성페이지 열기/    
    
    
    def sort(self,type_check,review_count,driver):
        if type_check == 'search':
            #최신순 청렬및 속성 리스트 펼치기 서치 쇼핑
            if review_count != 0:
                shnew_sort_check = ''
                passcount = 0
                while shnew_sort_check!='선택됨' :
                    if passcount == 5:
                        driver.refresh()
                    elif passcount == 10:
                        print('선택불가')
                        break
                    try:
                        new_sort = driver.find_element_by_css_selector('#section_review > div.filter_sort_group__Y8HA1 > div.filter_filter_box__iKVkl > div.filter_sort_box__223qy > a:nth-child(3)')
                        new_sorttext = new_sort.text
                        ActionChains(driver).move_to_element(new_sort).perform()
                        print(new_sorttext,'====정렬중')
                        if new_sorttext == '최신순':
                            try:
                                new_sort.click()
                            except:
                                new_sort.send_keys(Keys.ENTER)
                        shnew_sort_check = driver.find_element_by_css_selector('#section_review > div.filter_sort_group__Y8HA1 > div.filter_filter_box__iKVkl > div.filter_sort_box__223qy > a.filter_sort__1YUTp.filter_on__X0_Fb > span').text
                        print('최신순',shnew_sort_check)
                    except:
                        passcount = passcount+1
                        sleep(0.5)
                        pass
                # 속성 리스트 평치기
                try: 
                    
                    elem_full_list_btn = driver.find_element_by_class_name('filter_btn_more__1qzgF')
                    full_btn_text = elem_full_list_btn.text
                except:
                    full_btn_text = ''
                if full_btn_text == '펼치기':
                    cnt = 0
                    while full_btn_text =='펼치기':
                        print('속성 펼처기 버튼 클릭')
                        try:
                            try:
                                elem_full_list_btn.click()
                            except:
                                elem_full_list_btn.send_Keys(Keys.ENTER)
                            sleep(1)    
                            full_btn_text = driver.find_element_by_class_name('filter_btn_more__1qzgF').text
                            print('버튼 텍스트')
                            print(full_btn_text)
                        except:
                            sleep(0.5)
                            pass

        # 최신순 청렬 (스마트스토어)
        else:
            search_html = driver.page_source
            sortviewCheck = 0
            soup = bs(search_html, features="lxml")
            review_check_count = soup.select_one('strong._2pgHN-ntx6').get_text()
            print('===============================')
            print(review_check_count)
            if review_check_count!='0':
    #             sortlist = soup.select('div.WiSiiSdHv3 li')
    #             for i in range(1,len(sortlist)):
    #                 new_sorttext = sortlist[i].get_text()
    #                 print(new_sorttext)
    #                 if new_sorttext =='최신순':
    #                     sorti = i 
    #                     break
                for i in range(1,5):
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    sleep(1)
                sort_count = 0
                fail_count = 0
                while True:
                    if fail_count == 10:
                        print('최신순 정렬실패')
                        
                        break                                          #REVIEW > div > div.hmdMeuNPAt > div > div._1TvkeQbpJb > div._JEL2FoNN4 > ul > li:nth-child(2) > a  
                    try:                                              #REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a                                
                        try:
                            new_sort = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a')
                            sortviewCheck = 0
                        except:
                            new_sort = driver.find_element_by_css_selector('#REVIEW > div > div.hmdMeuNPAt > div > div._1TvkeQbpJb > div._JEL2FoNN4 > ul > li:nth-child(2) > a')
                            sortviewCheck = 1
                        new_sorttext = new_sort.text
                        if new_sorttext != '최신순':
                            print('최신순 검색실패 refresh')
                            driver.refresh()
    #                         sleep(2)                                        /html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div[6]/div/div[3]/div/div[1]/div[1]/ul/li[2]/a
                            try:
                                new_sort = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a')
                                sortviewCheck = 0
                            except:
                                new_sort = driver.find_element_by_css_selector('#REVIEW > div > div.hmdMeuNPAt > div > div._1TvkeQbpJb > div._JEL2FoNN4 > ul > li:nth-child(2) > a')
                                sortviewCheck = 1    
                            new_sorttext = new_sort.text
                            
                        try:
                            try:
                                move = driver.find_element_by_css_selector('#REVIEW > div > div._2gK-Ama9sJ > strong')
                            except:
                                move = driver.find_element_by_css_selector('#REVIEW > div > div._3iLs2V4Ln_ > div._3pRsbvMQEy.section_statistics > div > div > div._2Mt9yHWuNh > strong')
                                
                        except:
                            move = ''
                        if move != '':
                            ActionChains(driver).move_to_element(move).perform()
                        print(new_sorttext,'====정렬중')
                        if new_sorttext == '최신순':
                            new_sort.click()
                        if sortviewCheck == 0:
                            new_sort_check = driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a').get_attribute('aria-checked')
                        else:
                            new_sort_check = driver.find_element_by_css_selector('#REVIEW > div > div.hmdMeuNPAt > div > div._1TvkeQbpJb > div._JEL2FoNN4 > ul > li:nth-child(2) > a').get_attribute('aria-checked')
                            
                        print(new_sort_check)
                        if new_sort_check == 'true':
                            break
                        sort_count= sort_count+1
                        if sort_count == 5:
                            driver.refresh()
                    except:
                        fail_count = fail_count +1
                        sleep(0.5)
                        pass

    def search_shopping(self,title,item_code,productid,review_count,url):
        duplicateQs = NvReview.objects.filter(productid=productid)
        item_code = item_code
        productid = productid
        title = title
        driver = self.driveropen(url)
        review_list= []
        next_btn_text_dumy = 0
        #품절체크
        try:
            soldout_check = driver.find_element_by_xpath('/html/body/div/div/div[2]/h2')
            print(soldout_check.text)
            driver.quit()
    #         driver.close()
    #         first_tab = driver.window_handles[0]
    #         driver.switch_to.window(window_name=first_tab )
            return review_list
        except:
            pass
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #리뷰태그 선택
        
        
        
        sleep(0.5)
        reviewtag_html = driver.page_source
        rtsoup = bs(reviewtag_html, features="lxml")
        review_tag = rtsoup.select_one('div.floatingTab_detail_tab__2T3U7 > ul')
        if len(review_tag)==3:
            try:
                try:
                    review_tag = driver.find_element_by_css_selector('#snb > ul > li.floatingTab_on__299Bi > a').click()
                except:
                    review_tag = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div[2]/ul/li[2]/a').click()
            except:
                try:
                    review_tag = driver.find_element_by_css_selector('#snb > ul > li.floatingTab_on__299Bi > a').send_keys(Keys.ENTER)
                except:
                    return review_list
        else:
            try:
                try:
                    review_tag = driver.find_element_by_css_selector(' #snb > ul > li:nth-child(4) > a').click
                except:
                    review_tag = driver.find_element_by_css_selector('#snb > ul > li.floatingTab_on__299Bi').click()
            except:
                try:
                    review_tag = driver.find_element_by_css_selector('#snb > ul > li.floatingTab_on__299Bi').click()
                except:
        #             print('쇼핑몰리뷰 태그가 존재하지 않습니다.')
                    driver.quit()
    #                 driver.close()
    #                 first_tab = driver.window_handles[0]
    #                 driver.switch_to.window(window_name=first_tab )
                    return review_list
        
        
        #최신순 정렬
        type_check = 'search'
        self.sort(type_check,review_count,driver)
        sleep(2)
        print('정렬완료 검색 시작')

        next_btn_text = 1
        rv_count = 0
        paging_num = 2
        page = 1
        soup = ''
        soup_dumy = ''
        duplcate_state = ''
        for page in range(1,100):
            if duplcate_state == 'duplicate':
                break
            soup=''
            sleep(0.5)
            sleepRandom = rd.randint(1,10)
            slp = round(rd.uniform(0.8,1),2)
            if paging_num==sleepRandom:
                sleep(slp)
            review_html = driver.page_source
            soup = bs(review_html, features="lxml")
            if soup==soup_dumy:
                for i in range(2):
                    sleep(0.5)
                    review_html = driver.page_source
                    soup = bs(review_html, features="lxml")
            soup_dumy = soup
            try:
                reviewList =soup.select('ul.reviewItems_list_review__1sgcJ li')
            except:
                break
            i=1
    #             
            
            Random = rd.randint(1,10) 
            if Random == sleepRandom:
                sleep(slp)
            for review in reviewList:
                reviewinfo = review.select('div.reviewItems_etc_area__2P8i3 span')
                review_text = review.select_one('p.reviewItems_text__XIsTc').get_text()
                review_text = review_text.replace(',','')
                review_text = review_text.replace('\n','')
                review_content=review_text.replace("[^0-9 가-힣 a-z A-Z ]", "")
                user_star = reviewinfo[0].get_text().replace('평점','')
                seller = reviewinfo[3].get_text()
                user_name = reviewinfo[4].get_text()
                review_create_date = reviewinfo[5].get_text()
                try:
                    item_option = reviewinfo[6].get_text()
                except:
                    item_option = ' '


                rv_count = rv_count+1
                additem =[item_code,productid,title,item_option,user_star,review_content,user_name,review_create_date ]
                review_list.append(additem)
                review_check = ''
                review_check = duplicateQs.filter(title__icontains=title,user_name__icontains=user_name,review_create_date__icontains=review_create_date,review_content__icontains=review_content)
                if review_check:
                    duplcate_state = 'duplicate'
                    break    
                else:
                    NvReview(item_code = item_code, productid = productid,title=title,item_option=item_option,user_name=user_name,
                    user_star=user_star,review_create_date=review_create_date,review_content=review_content).save()
            sleep(0.7)
            RRandom = rd.randint(1,10) 
            if RRandom == sleepRandom:
                sleep(slp)
            if next_btn_text != 1:
                try:
                    if next_btn_text%10 ==1:
                        paging_num = 3
                except:
                    print(next_btn_text,'출력')


            paging_num =str(paging_num)
            try:
                next_btn_text_dumy = int(next_btn_text)
    #                 next_btn_text = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a['+paging_num+']').text
                next_btn_text = driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 > a:nth-child('+paging_num+')').text          
                if next_btn_text=='다음':
                    next_btn_text = next_btn_text_dumy + 1
                    if next_btn_text == 101:
                        break
                else:
                    next_btn_text = int(next_btn_text)
    #                 next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a['+paging_num+']')    
                next_btn = driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 > a:nth-child('+paging_num+')')         
                try:
                    try:
                        next_btn.click()
                    except:
                        next_btn.send_keys(Keys.ENTER)
                except:
                    try:
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[7]/div[3]/a['+paging_num+']').click()
                    except:
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[7]/div[3]/a['+paging_num+']').send_keys(Keys.ENTER)
            except:
                try:
                    try:
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a['+paging_num+']').send_keys(Keys.ENTER)  
                    except:
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a['+paging_num+']').click()

                except:
                    break
            paging_num = int(paging_num)
            paging_num = paging_num+1
            #페이징처리 조건
        print(f'최종페이지 ==={next_btn_text}')   
        driver.quit()
    #     driver.close()
    #     first_tab = driver.window_handles[0]
    #     driver.switch_to.window(window_name=first_tab )
        return review_list





    def smart_shopping(self,title,item_code,productid,review_count,url):
        duplicateQs = NvReview.objects.filter(productid=productid)
        driver = self.driveropen(url)
        item_code = item_code
        productid = productid
        title = title
        next_btn_text_dumy = 0
        review_list= []
        for i in range(5):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(0.5)
        try:                                          
            try:
                review_tag = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div[3]/ul/li[2]').click()
            except:
                review_tag = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div[5]/div/div[3]/ul/li[2]').click()
        except:
            try:
                try:
                    review_tag = driver.find_element_by_css_selector('#_productTabContainer > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2)').click()
                except:
                    review_tag = driver.find_element_by_css_selector('#_productTabContainer > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2)').click()
            except:
    #             print('쇼핑몰리뷰 태그가 존재하지 않습니다.')
                driver.quit()
                return review_list
        
        # 리뷰가 존재할시 최신순 청렬 (스마트스토어)
        type_check = 'smart'
        self.sort(type_check,review_count,driver)
        try:
            seller = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div/div[1]/h1/a/span').text
        except:
            seller = ''
        #속성
        sleep(2)
        search_html = driver.page_source
        soup = bs(search_html, features="lxml")
        title_text = soup.select_one('h3._3oDjSvLwq9').get_text()
        print(title_text)
        
        review_count = int(soup.select_one('strong._2pgHN-ntx6').get_text().replace(',',''))
        
            
        #아이템 속성
        elem_count = 1
        

        next_btn_text=1
        rv_count = 0
        us = url.find('shopping.naver')
        uu = url.find('smartstore.naver')
        if us != -1:
            paging_num = 2
        else:
            paging_num = 3
        page = 1
        rsoup_dumy = ''
        rsoup = ''
        last_page = (review_count//20)+1
        duplcate_state = ''
        for page in range(1,last_page+1):
            if duplcate_state == 'duplicate':
                break
            sleepRandom = rd.randint(1,10)
            slp = 0.5
    #             slp = round(rd.uniform(0.5,1),2)
            if paging_num==sleepRandom:
                sleep(slp)
            review_html = driver.page_source
            rsoup = bs(review_html, features="lxml")
            if rsoup==rsoup_dumy:
                for i in range(2):
                    sleep(0.5)
                    review_html = driver.page_source
                    rsoup = bs(review_html, features="lxml")
            rsoup_dumy = rsoup
            print('=======================')
            #쇼핑.네이버 일경우 체크 ===========
            ck_review = 0
            reviewList =rsoup.select('ul.TsOLil1PRz li')
            if len(reviewList)==0:
                reviewList = rsoup.select('ul._1iaDS5tcmC div._2B-RlWYmaK')
                ck_review = 1
            #===================================
            i=1
            elem_name = '주제전체'
            if ck_review ==0:
                for review in reviewList:
                    user_star = review.select_one('em._15NU42F3kT').get_text()
                    try:
                        item_option = review.select_one('button._3jZQShkMWY > span').get_text()
                    except:
                        item_option = '    '
                    user_name = review.select_one('strong._3QDEeS6NLn').get_text()
                    review_create_date = review.select_one('span._3QDEeS6NLn').get_text()
                    review_text = review.select_one('div.YEtwtZFLDz').get_text()
                    review_text = review_text.replace(',',' ')
                    review_text = review_text.replace('\n','')
                    review_text = review_text.replace('한달사용기','')
                    review_content=review_text.replace("[^0-9 가-힣 a-z A-Z ]", "")
                    seller = seller.replace('\n','')
                    url = url
                    rv_count = rv_count+1
                    additem =[item_code,productid,title,item_option,user_star,review_content,user_name,review_create_date ]
                    review_list.append(additem)
                    # review_check = []
                    # review_check = duplicateQs.filter(title__icontains=title,user_name__icontains=user_name,review_create_date__icontains=review_create_date,review_content__icontains=review_content)
                    # if review_check:
                    #     duplcate_state = 'duplicate'
                    #     break    
                    # else:
                    NvReview(item_code = item_code, productid = productid,title=title,item_option=item_option,user_name=user_name,
                    user_star=user_star,review_create_date=review_create_date,review_content=review_content).save()
        #                 print(rv_count)#===
            else:
                for review in reviewList:
                    user_star = review.select_one('em._15NU42F3kT').get_text()
                    try:
                        item_option = review.select_one('button.NIYM68WJ2v > span').get_text()
                    except:
                        item_option = '    '
                    user_name = review.select_one('strong._2Xe0HVhCew').get_text()
                    review_create_date = review.select_one('span._2Xe0HVhCew').get_text()
                    review_text = review.select_one('div._3AGQlpCnyu span._2Xe0HVhCew').get_text()
                    review_text = review_text.replace(',',' ')
                    review_text = review_text.replace('\n','')
                    review_text = review_text.replace('한달사용기','')
                    review_content=review_text.replace("[^0-9 가-힣 a-z A-Z ]", "")
                    seller = seller.replace('\n','')
                    url = url
                    rv_count = rv_count+1
                    additem =[item_code,productid,title,item_option,user_star,review_content,user_name,review_create_date ]
                    review_list.append(additem)
                    # review_check = []
                    # review_check = duplicateQs.filter(title__icontains=title,user_name__icontains=user_name,review_create_date__icontains=review_create_date,review_content__icontains=review_content)
                    # if review_check:
                    #     duplcate_state = 'duplicate'
                    #     break    
                    # else:
                    NvReview(item_code = item_code, productid = productid,title=title,item_option=item_option,user_name=user_name,
                    user_star=user_star,review_create_date=review_create_date,review_content=review_content).save()

        #                 print(rv_count)#===
                
            sleep(1)
            RRandom = rd.randint(1,10) 
            if RRandom == sleepRandom:
                sleep(slp)
            if next_btn_text != 1:
                if us == -1:
                    if next_btn_text%10 ==1:
                        paging_num = 3
            
            if uu != -1:
                paging_num = str(paging_num)
                try:
                    next_btn_text_dumy = int(next_btn_text)           
                    try:                                              
                        next_btn_text = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div[6]/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']').text     
                        btni='6'
                    except:
                        next_btn_text = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div[7]/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']').text
                        btni='7'
                    if next_btn_text=='다음':
                        next_btn_text = next_btn_text_dumy + 1
                    elif next_btn_text == '':
                        next_btn_text = next_btn_text_dumy
                    else:
                        next_btn_text = int(next_btn_text)
                    next_btn = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div['+btni+']/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']')
                    next_btn.click()
                except:
                    try:
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div['+btni+']/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']').send_keys(Keys.ENTER)  
                    except:
                        break
                paging_num = int(paging_num)
                paging_num = paging_num+1
                #페이징처리 조건
            elif us != -1:     #shooping.com 일때
                print(paging_num)
                if paging_num > 6:
                    paging_num = 7
                paging_num = str(paging_num)
                try:
                    next_btn_text_dumy = int(next_btn_text)           
                    next_btn_text = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[6]/div[4]/div/div[3]/div/div[2]/a['+str(paging_num)+']').text
                
                    if next_btn_text=='다음':
                        next_btn_text = next_btn_text_dumy + 1
                    elif next_btn_text == '':
                        next_btn_text = next_btn_text_dumy     
                    else:                                      
                        next_btn_text = int(next_btn_text)    
                    next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[6]/div[4]/div/div[3]/div/div[2]/a['+str(paging_num)+']')
                    next_btn.click()
                except:                                    
                    try:                                   
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[6]/div[4]/div/div[3]/div/div[2]/a['+str(paging_num)+']').send_keys(Keys.ENTER)  
                    except:
                        break
                paging_num = int(paging_num)
                paging_num = paging_num+1
                #페이징처리 조건
                
            else:
                paging_num = str(paging_num)
                try:
                    next_btn_text_dumy = int(next_btn_text)           
                    try:                                              
                        next_btn_text = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div/div[3]/div[6]/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']').text
                        btni='6'
                    except:
                        next_btn_text = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div/div[3]/div[7]/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']').text
                        btni='7'
                    if next_btn_text=='다음':
                        next_btn_text = next_btn_text_dumy + 1
                    elif next_btn_text == '':
                        next_btn_text = next_btn_text_dumy
                    else:
                        next_btn_text = int(next_btn_text)
                    next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div/div[3]/div['+btni+']/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']')
                    next_btn.click()
                except:
                    try:
                        next_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div/div[3]/div['+btni+']/div/div[3]/div/div[2]/div/div/a['+str(paging_num)+']').send_keys(Keys.ENTER)  
                    except:
                        break
                paging_num = int(paging_num)
                paging_num = paging_num+1
                #페이징처리 조건
                    
                                
        print(f'최종페이지 ==={next_btn_text}')    
        driver.quit()
    #     driver.close()
        return review_list    

            
        

