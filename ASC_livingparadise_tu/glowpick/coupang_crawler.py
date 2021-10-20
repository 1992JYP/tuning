## 수정  2021- 10-05이유인

from django.shortcuts import render
from numpy import product
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
from datetime import datetime,timedelta
import re
import os
import pandas as pd
from tqdm import tqdm
from .models import CategoriCmk,CmkCpProduct,CmkCpReview
from time import sleep
from selenium import webdriver
import chromedriver_autoinstaller
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

class CcoupangCrawler:
        

    def __init__(self):
        self.today = datetime.now()
        self.yesterday = self.today- timedelta(1)
        self.today = self.today.strftime("%Y-%m-%d")
        print(self.today)
        self.yesterday = self.yesterday.strftime("%Y-%m-%d")
        self.base_cp_url = 'https://www.coupang.com/'
        self.item_search_base_url = 'https://www.coupang.com/np/categories/{}?page={}'  # 기본설정 60개 
        self.review_base_url = 'https://www.coupang.com/vp/product/reviews?productId={}&page={}&size=100&sortBy=DATE_DESC'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
        patht = f'./{chrome_ver}/chromedriver.exe'
        
        try:
            driver = webdriver.Chrome(patht,options=options)   
        except:
            chromedriver_autoinstaller.install(True)
            driver = webdriver.Chrome(patht,options=options)
        url = 'http://www.useragentstring.com/'
        driver.get(url)
        user_agent = driver.find_element_by_id('uas_textfeld').text
        user_agent = user_agent.replace('Headless','')
        driver.quit()

        self.headers = {
        'User-Agent' : user_agent
        }
        print(user_agent)
        


    def categori_listup(self):
        qs = CategoriCmk.objects.all()
        qs = qs.filter(~Q(coupang_cids=''))
        cp_list = []
        search_list = []
        for q in qs.values_list():
            cp_list.append(q)
        
        
        for li in cp_list:
            cid_list = []
            cmk_id = li[0]
            second_class_name = li[8]
            cid_list = li[5].split(',')
            search_list.append([cmk_id,second_class_name,cid_list])

        return search_list


    def item_search(self): 
        full_item_list = []   
        search_list = self.categori_listup()
        for categori in tqdm(search_list, position=0, desc='카테고리별 상품정보 크롤링'):
            checkbool = False
            cid_list = categori[2]
            max_item = 100//len(cid_list)
            print(cid_list)
            for cid in cid_list:
                item_list = []
                print(cid)
                itemcount = 0
                #last_page 뽑아오기
                url = self.item_search_base_url.format(cid,'1')
                res = requests.get(url, headers=self.headers)
                if res.status_code == 200:
                    soup = bs(res.text,features="lxml")
                    try:
                        last_page = soup.select('div.page-warpper a')
                        last_page = len(last_page)
                    except:
                        last_page = 1
                error_cnt = 0
                if last_page>3:
                    last_page = 3
                last_page = last_page
                item_list = self.item_info_search(categori,last_page,cid,max_item)
                full_item_list = full_item_list + item_list
        
        state = self.item_list_saveCSV(full_item_list)
        print('엑셀저장 = ',state)
    



    def item_info_search(self,categori,last_page,cid,max_item):
        cmk_id = categori[0]
        second_class_name = categori[1]
        date_info = self.today
        item_check_num = 1
        noAddNum=0          #광고제거 아이템 개수 체크
        error_list = []
        item_count = 0
        max_item = max_item
        for page in range(1,last_page):   
            if item_count == max_item:
                break
            noAD_list = []     #
            url = self.item_search_base_url.format(cid,page)
            res = requests.get(url, headers=self.headers)
            print(url)
            if res.status_code == 200:
                soup = bs(res.text,features="lxml")
                item_list = soup.select('ul#productList li')
                cp_class = soup.select_one('h3.newcx-product-list-title').get_text().replace('\n','').replace('\t','').replace(' ','')
                print(cp_class)
                for item in item_list:
                    if item_count == max_item:
                        break
                    try:
                        adCheck = item.select_one('span.ad-badge-text').get_text()
                    except:
                        adCheck = '상품'
                    try:
                        
                        title = item.select_one('div.name').text.strip()
                        link = item.select_one('a').get('href')
                        url = parse.urljoin(self.base_cp_url, link)
                        itemres = requests.get(url, headers=self.headers)
                        if itemres.status_code != 200:
                            print(url)
                            print(itemres)
                        if itemres.status_code == 200:
                            itemsoup = bs(itemres.text,features="lxml")
                            try:
                                imgpath = itemsoup.select_one('img.prod-image__detail').get('src')
                                imgpath = 'https:'+imgpath
                            except:
                                imgpath = ''
                            try:
                                brand = itemsoup.select_one('a.prod-brand-name').get_text()
                            except:
                                brand = ''
                            det_list = itemsoup.select('ul.prod-description-attribute li')
                            detail = ''
                            for li in det_list:
                                detai = li.get_text().replace(' ','')
                                
                                if detai.find('쿠팡상품번호') != -1:
                                    productid = detai.replace('쿠팡상품번호:','')
                                    break
                                detail = detail+'-'+detai
                        try:
                            grade = item.select_one('em.rating').get_text()
                        except:
                            grade = '0'
                        try:
                            price = item.select_one('strong.price-value').text.strip()
                            price = ''.join(price.split(','))
                        except:
                            price = '0'
                        try:
                            review_count = item.select_one('span.rating-total-count').text.strip()
                            review_count =  re.sub("\(|\)","",review_count)
                        except:
                            review_count = '0'
                        if adCheck == '상품':
                            ranking = item_check_num
                            item_check_num = item_check_num+1
                            ### 광고 제거한 리스트목록  ###
                            noAddNum = noAddNum+1
                            item_info = [cmk_id,second_class_name,cp_class,productid,title,ranking,price,grade,review_count,brand,detail, url, imgpath,date_info]
                            try:
                                CmkCpProduct(cmk_id = cmk_id, second_class_name = second_class_name, cp_class = cp_class, productid = productid,
                                title = title, ranking = ranking, price=price, grade = grade, review_count = review_count, brand = brand,detail = detail,
                                url=url, imgpath = imgpath, date_info=date_info).save()
                                noAD_list.append(item_info)  #광고를 제회한 전체 리스트목록
                                item_count = item_count+1
                            except:
                                
                                print('saveerror')                    

                    except:
                        error_item = [cmk_id,cp_class,cid]
                        error_list.append(error_item)
                        print('error_check')
                        # error_cnt+1
                
            



        return noAD_list   
    
    
    # 쿠팡 평점 변환 
    def grade_change(self, percent):
        if percent == '100':
            grade = '5'
        elif percent == '90':
            grade = '4.5'
        elif percent == '80':
            grade = '4'
        elif percent == '70':
            grade = '3.5'
        elif percent == '60':
            grade = '3'
        elif percent == '50':
            grade = '2.5'
        elif percent == '40':
            grade = '2'
        elif percent == '30':
            grade = '1.5'
        elif percent == '20':
            grade = '1'
        elif percent == '10':
            grade ='0.5'
        else:
            grade = '0'

        return grade 

    def review_search(self):
        item_list = self.review_serarch_list()
        # item_info = [cmk_id,second_class_name,cp_class,productid,title,ranking,price,grade,review_count,brand,detail, url, imgpath,date_info]
        review_list = []
        passCnt = 0

        for item  in tqdm(item_list, position=0, desc='review_crawling'):
            cmk_id = item['cmk_id']
            cp_class= item['cp_class']
            productid = item['productid']
            # select = productid.find('-')
            # productid = productid[0:select]
            title = item['title']
            pidck = productid.find('-')
            pid = productid[0:pidck]
            page = int(item['review_count'])//100
            page = page+1
            if page > 30:
                page = 30
            ci = 1

            review_qs = CmkCpReview.objects.filter(productid__icontains=productid)
            ckRiview_state = '' 
            
            for ci in range(ci,page+1):
                if ckRiview_state == 'overrap':
                    break
                url = self.review_base_url.format(pid,ci)
                res = requests.get(url, headers=self.headers)
                if res.status_code == 200:
                    soup = bs(res.text,features="lxml")
                    rv_list = []
                    rv_list = soup.select('article.sdp-review__article__list')
    #                 img_list = soup.select('div.sdp-review__article__list__attachment__list')   <<<<<<<<<<<<  review img
                    for review in rv_list:
                        user_name = review.select_one('span.sdp-review__article__list__info__user__name').text.strip() 
                        review_create_date = review.select_one('div.sdp-review__article__list__info__product-info__reg-date').text.strip()
                        option = review.select_one('div.sdp-review__article__list__info__product-info__name').text.strip()
                        user_star = review.select_one('div.js_reviewArticleRatingValue').get('data-rating')
                        headline = review.select_one('div.sdp-review__article__list__headline')  
                        #When trying to get text, get an error tag and remove the tag using regular expression after replacing str
                        headline = str(headline)        
                        headline = re.sub('(<([^>]+)>)', '', headline)   
                        headline = headline.replace("\n","").replace(" ","")
                        headline = headline.replace("None","")
                        try:
                            content = review.select_one('div.js_reviewArticleContent').text.strip()
                            content = content.replace("\n","")
                        except:
                            content = review.select_one('div.js_reviewArticleContent')
                            content = str(content)
                            content = content.replace("\n","").replace(" ","")
                            content = content.replace("None","")
                        review_content = headline + content
                        review_content=review_content.replace("[^0-9 가-힣 a-z A-Z ]", "")
                        if review_content != "":
                            ckRiview = []
                            review_create_date = review_create_date.replace('.','-')

                            ckRiview =  review_qs.filter(cmk_id__icontains=cmk_id,productid__icontains=productid,
                            title__icontains=title,user_name__icontains=user_name, review_create_date__icontains=review_create_date,
                            user_star__icontains=user_star,option__icontains=option, review_content__icontains=review_content)
                            if ckRiview:
                                ckRiview_state = 'overrap'
                                break
                            else:
                                ckRiview_state = 'new'
                                review_list.append([cmk_id,productid,title,user_name,review_create_date,user_star,option,review_content])
                            
                            try:
                                CmkCpReview(cmk_id=cmk_id,productid =productid,title=title,user_name = user_name, 
                                review_create_date = review_create_date,
                                user_star = user_star, option = option,review_content = review_content).save()
                            except:
                                passCnt = passCnt +1
                                pass
        newReviewCount = len(review_list)
        

        filename = 'coupang_review_{}.csv'.format(self.today)
        filepath ='C:/Croling/cosmeca/coupang/'+ filename                    
        df = pd.DataFrame(review_list, columns=['cmk_id','productid','title','user_name','review_create_date','user_star','option','review_content'])
        df.to_csv(filepath, index=False, encoding='utf-8')   
        
        insertCnt = newReviewCount - passCnt
        print("new  review searching " , newReviewCount, )
        print("save failed ", passCnt, )
        print("save succes : " , insertCnt, )
        
        if newReviewCount <= 30:
            print(review_list)
        
        return review_list

        
        
        
        
    def item_list_saveCSV(self, full_item_list):
        
        filename = 'ProductSearchResult_{}.csv'.format(self.today)
        filepath ='C:/Croling/cosmeca/coupang/'+ filename

        df = pd.DataFrame(full_item_list, columns=['cmkid','second_class_name','cp_class','productid',
        'title','ranking','price','grade','review_count','brand','detail','url','imgpath','date_info'])
        try:
            df.to_csv(filepath, index=False, encoding='utf-8') 
            state = 'success'
        except:
            print('save_error')
            state = 'faile'
        return state            



        
        

    def review_serarch_list(self):
        item_list = []
        qs = CmkCpProduct.objects.filter(date_info__icontains=self.today).values()
        for item in qs.values():
            item_list.append(item)
        
        
        return item_list