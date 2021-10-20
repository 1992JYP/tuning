## 작성 2021-06-22  - 이유인 
## 수정  2021- 09-27  - 이유인

from django.shortcuts import render
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
from datetime import datetime,timedelta
import re
import os
import pandas as pd
from .models import Cp_c_Product , Cp_review, ProductState
from apps.paradise.models import ProductMaster
from tqdm import tqdm
from time import sleep
from selenium import webdriver
import chromedriver_autoinstaller
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

class coupangCrawler:
        

    def __init__(self):
        #pid 목록 excel file name / sheet name / 검색키워드 담을 리스트 
        self.excelfile_name = '매칭키워드_정리_URL 매칭.xlsx'
        self.excelsheet_name = 'Sheet1'
        self.keyword_list = []
        #상품 검색 개수 
        self.otherlastItemCheck = 3
        #아이템 광거제거 목록 / 광고포함목록/ 리뷰목록 / 체크url목록
        self.noAD_list = []
        
        self.result_list = []
        self.review_list = []
        self.ck_url_list=[]
        self.otheritem = []
        self.my_itemreview_list = []
        self.today = datetime.now()
        self.yesterday = self.today- timedelta(1)
        self.today = self.today.strftime("%Y-%m-%d")
        print(self.today)
        self.yesterday = self.yesterday.strftime("%Y-%m-%d")
        
        
        try:
            self.yesterdf = pd.read_csv('C:/Croling/living_paradise/Coupang/ProductSearchResult_'+self.yesterday+'.csv')
        except:
            print('전일 데이터 load error')
            pass
       
        self.item_search_base_url = 'https://www.coupang.com/np/search?q={}&page={}'
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
    # db 연결 실패시 백업파일 저장 및 백업파일 존재시 누락 데이터 저장 
    def backup_data_search(self):
        try:
            backupitem = pd.read_csv('C:/Croling/living_paradise/Coupang/db_down_backup/ProductSearchResult_'+self.yesterday+'.csv')
            backupitem_list = backupitem.values.tolist()

            print('====================yesterday item data omission Saving==============')
            for item in backupitem_list:
                Cp_c_Product(keyword =item[0], pd_index = item[1],change_index = item[2], company = item[3], pc_code = item[4] ,title = item[5], state = item[6],page_link = item[7],
                        product_id = item[8], price = item[9], review_count = item[10],
                        image_link = item[11], item_id = item[12], grade = item[13], date_info= item[14]).save()

            print('=============================Saved===============================')
            try:
                print('=====================Delete the file =====================')
                os.remove('C:/Croling/living_paradise/Coupang/db_down_backup/ProductSearchResult_'+self.yesterday+'.csv')
                
                print('ProductSearchResult_'+self.yesterday+'.csv 파일 삭제 완료 ')
            except:
                print('=======================파일 삭제 실패 =========================')
                
            
            backupreview = pd.read_csv('C:/Croling/living_paradise/Coupang/db_down_backup/review_'+self.yesterday+'.csv')
            backupreview_list = backupreview.values.tolist()

            print('====================전일 리뷰 데이터 누락 사항 저장중==============')

            qs = Cp_review.objects.all()


            for review in backupreview_list:
                ckReview = []
                ckReview =  qs.filter(product_id__icontains=review[0],user_name__icontains=review[1],title__icontains=review[4], date__icontains=review[2], review__icontains=review[5])
                
                if ckReview:
                    break
                else:
                    Cp_review(product_id =review[0], user_name = review[1], date = review[2],grade = review[3], title = review[4],
                                        review = review[5]).save()
        except:
            print('===========================전일 누락 사항 없음 =================================')
            pass
        



    def search_listup(self):
        try:
            item_list =[]
            # 자사 상품목록 가져오기 
            try:
                qs = ProductMaster.objects.all()
                for s in qs.values_list():
                    item_list.append(s)
                df = pd.DataFrame(item_list, columns=['ID','담당','품목코드','품목명','브랜드','매칭키워드','네이버코드','네이버URL','쿠팡코드','쿠팡URL','이미지'])
                self.dbstate = 'success'
                print(self.dbstate)
                print('DB 접속 =====================', self.dbstate,'=====================')
            except:
                # db접속안될시 excel 파일
                df = pd.read_excel(io='C:/Croling/living_paradise/'+self.excelfile_name, sheet_name=self.excelsheet_name)
                self.dbstate = 'faile'
            
            df = df.dropna(subset=['쿠팡URL','매칭키워드'])  #결측치 제거
            matchingKeyword = df['매칭키워드']
            matchingKeyword = matchingKeyword.drop_duplicates()  #중복제거
            matchingKeyword=matchingKeyword.values.tolist()
            

            # 여러개 행을 선택할때 loc 사용
            url_list = df.loc[:,['품목코드','쿠팡URL']]
            url_list = url_list.values.tolist()
            self.df = df.values.tolist()
            




            # url_list = df.values.tolist()
            #검색 키워드 리스트 뽑기
            
            for item in matchingKeyword:
                self.keyword_list.append(item)
            #체크 url 리스트
            for item in url_list:
                last_index = item[1].find('&q=')
                pd_code = item[0]
                url = item[1][:last_index]
                self.ck_url_list.append([url,pd_code])
        except:
            print('상품정보를 가져오는데 실패 하였습니다.')
            self.keyword_list = ['']
        return self.keyword_list
        

    def item_search(self):    
        self.myItem = []
        self.sumItem = []
        
        for key in tqdm(self.keyword_list, position=0, desc='상품 정보 크롤링'):
            checkbool = False
            keyword = key 
            if keyword == None:    #결측시 방샐지 pass
                continue

            itemcount = 0
            #검색어별 자사 상품 개수
            
            for item in self.df:
                if item[5]==keyword:
                    itemcount=itemcount+1
            print(keyword +'자사상품개수  = ', itemcount,' 개')
            
            #last_page 뽑아오기
            url = self.item_search_base_url.format(keyword,1)
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                soup = bs(res.text,features="lxml")
                try:
                    last_page = soup.select_one('a.btn-last').text.strip()
                except:
                    last_page = '1'
            # 위에서 조회한 마지막 페이지까지 저회후 아이템 이름/링크/가격 저장
            # urllib.parse.urljoin() >> base_url과 url을 URL형식으로 합쳐줌
            # product id 담음
            error_cnt = 0
            item_num = 1
            item_check_num = 1
            #이미지 링크 생성 베이스
            cp_url = 'https://www.coupang.com/'
            otherCheck = 0      #다른회사 아이템 개수 체크
            myitemCheck = 0     #생활낙원 아이템 개수 체크
            allItemNum = 0      #전체 아이템 개수 체크
            noAddNum=0          #광고제거 아이템 개수 체크
            last_page = int(last_page)
            if last_page>11:
                last_page = 11
            for page in range(1,last_page+1):        # 전체 상품 크롤링시  위의 last_page 활용 하여 돌리기  int(last_page)+2
                # if  item_check_num == self.lastItemCheck:    # 아이템 10개씩만 가져오기위해 넣은 조건문 제한 없을시 제거 
                #     break                                           
                #자회사 제품 전부와 다른회사 제품 3개 크롤링 완료시 다음 키워드로
                # if itemcount==myitemCheck and otherCheck==3:
                #             break                    
                url = self.item_search_base_url.format(keyword,page)
                res = requests.get(url, headers=self.headers)
                if res.status_code == 200:
                    soup = bs(res.text,features="lxml")
                    item_list = soup.select('ul#productList li')
                    for item in item_list:
                        try:
                            adCheck = item.select_one('span.ad-badge-text').get_text()
                        except:
                            adCheck = '상품'
                        try:
                            state = item.select_one('div.out-of-stock').get_text()
                            if state=='일시품절':
                                state = '일시품절'
                            else:
                                state = '품절'    
                        except:
                            state = '판매중'
                        try:
                            vendor_itemId = item.select_one('a').get('data-vendor-item-id')
                            item_name = item.select_one('div.name').text.strip()
                            link = item.select_one('a').get('href')
                            link = parse.urljoin(cp_url, link)
                            # 링크 비교 
                            for url in self.ck_url_list:
                                if url[0]==link:
                                    checkbool = True
                                    pd_code = url[1]
                                    company = 0
                                    break
                                else:
                                    checkbool = False
                                    company = 1
                                    pd_code = ''
                            imgres = requests.get(link, headers=self.headers)
                            if res.status_code == 200:
                                imgsoup = bs(imgres.text,features="lxml")
                                image_path = imgsoup.select_one('img.prod-image__detail').get('src')
                                image_path = 'https:'+image_path
                            try:
                                score = item.select_one('em.rating').get_text()
                            except:
                                score = '0'
                            pid = item.select_one('a').get('data-product-id')
                            price = item.select_one('strong.price-value').text.strip()
                            price = ''.join(price.split(','))
                            try:
                                review_count = item.select_one('span.rating-total-count').text.strip()
                                review_count =  re.sub("\(|\)","",review_count)
                            except:
                                review_count = '0'
                            if adCheck == '상품':
                                item_num = item_check_num
                                item_check_num = item_check_num+1
                                ### 광고 제거한 리스트목록  ###
                                # 어제날자 구함
                                
                                try:
                                    #전일 저장된 상품정보 파일 에서 상품 순위 로드후 순위변동 계산
                                    yesterdayItem = self.yesterdf['상품명'] == item_name
                                    yesterdayItem = self.yesterdf[yesterdayItem]
                                    yesterdayItem = yesterdayItem.values.tolist()
                                    change_index = int(yesterdayItem[0][1]) - item_num 
                                except:
                                    change_index = 9999
                                
                                noAddNum = noAddNum+1
                                self.noAD_list.append([keyword,item_num,change_index,company,pd_code,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score,self.today])  #광고를 제회한 전체 리스트목록
                                

                                if checkbool:
                                    # self.myItem.append([keyword,item_num,change_index,company,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score])  #생활낙원 제품 목록
                                    self.sumItem.append([keyword,item_num,change_index,company,pd_code,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score,self.today])
                                    if self.dbstate == 'success':
                                        duplicate = Cp_c_Product.objects.filter(pd_code__icontains=pd_code,keyword__icontains=keyword,title__icontains=item_name,date_info__icontains=self.today)
                                        if len(duplicate) ==0:
                                            Cp_c_Product(keyword =keyword, pd_index = item_num,change_index = change_index, company = company, pd_code=pd_code ,state = state, title = item_name, page_link = link,
                                                    product_id = pid, price = price, review_count = review_count,
                                                    image_link = image_path, item_id = vendor_itemId, grade = score, date_info = self.today).save()
                                    myitemCheck = myitemCheck+1
                                    print('생확낙원 제품 save', myitemCheck,'/',itemcount)
                                else:
                                    self.otheritem.append([keyword,item_num,change_index,company,pd_code,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score,self.today])
                                    
                                    if otherCheck <3:
                                        self.sumItem.append([keyword,item_num,change_index,company,pd_code,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score,self.today])
                                        if self.dbstate == 'success':
                                            Cp_c_Product(keyword =keyword, pd_index = item_num,change_index = change_index, company = company, pd_code=pd_code , state = state, title = item_name, page_link = link,
                                                    product_id = pid, price = price, review_count = review_count,
                                                    image_link = image_path, item_id = vendor_itemId, grade = score, date_info = self.today).save()
                                        
                                        otherCheck = otherCheck+1
                                        print('다른회사제품 save', otherCheck, '  개')
                            # self.result_list.append([keyword, allItemNum,item_name, link,pid, price,review_count,image_path,vendor_itemId,score])  #광고 포함 총 목록
                            allItemNum = allItemNum+1
                        except:
                            error_cnt+1
        



        filename = 'ProductSearchResult_{}.csv'.format(self.today)
        filepath ='C:/Croling/living_paradise/Coupang/'+ filename
        df = pd.DataFrame(self.noAD_list, columns=['키워드','상품랭킹','아이템순위변동','제조사','상품코드','상품명','판매상태','상품링크','상품아이디','가격','리뷰개수','이미지링크','아이템아이디','평점','검색일'])
        try:
            df.to_csv(filepath, index=False, encoding='utf-8') 
        except:
            print('save_error')
        if self.dbstate == 'faile':  #디비접속이안될시 백업 
            filepath = 'C:/Croling/living_paradise/Coupang/db_down_backup/'+ filename   
            try:
                df.to_csv(filepath, index=False, encoding='utf-8') 
            except:
                print('save_error')
                pass


        print('광고 포함 총 상품 개수 : ' , allItemNum ,' 개')
        print('광고 제거  총 상품 개수 : ' ,noAddNum ,' 개')
        # print('생활낙원  총 상품 개수 : ' ,len(self.myItem) ,' 개')

        # print('생활낙원  총 상품 개수 : ' ,len(self.myItem) ,' 개')
        return self.sumItem    
    

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


    
    # ============================================ 931가지 아이템 체크
    def my_allItem(self):
        #자사 상품 전체 리뷰리스트
        
        #db가 연결되어있을때 실행
        if self.dbstate == 'success':
            yqs= ProductState.objects.filter(mall_name__icontains='coupang')
            if yqs:
                try:
                    yqs.delete()
                    print('전일데이터 삭제 성공')
                except:
                    print('전일데이터 삭제 실패')
                    pass


            # 오늘자 검색된 자사 상품 리스트 db에서 가져옴 (랭킹정보활용)
            qs = Cp_c_Product.objects.all()
            today = self.today
            qs= qs.filter(company__icontains=0,date_info__icontains=today)
            print(today)
            dblist = []
            for s in qs.values_list():
                dblist.append(s)



            # 마스터 db에서 자사 상품 리스트 전체 가져오기 
            try:
                myitem_list = []
                mqs = ProductMaster.objects.all()
                for s in mqs.values_list():
                    myitem_list.append(s)

            except:
                print('error')
            
            # 전체 상품 list 가져오기 
            df = pd.DataFrame(myitem_list, columns=['ID','PD_MANAGER','PD_CODE','PD_NAME','PD_BRAND','PD_KEYWORD','NV_CODE','NV_URL','CP_CODE','CP_URL','IMAGE'])
            dff = df.fillna('없음')
            all_itme_list = df.values.tolist()
            id = 0
            full_list = []
            mall_name = 'coupang'
            for item in tqdm(all_itme_list):
                id= id+1

                myitem = []
                curl = item[9]
                if curl == None:
                    curl = ''
                nurl = item[7]
                if nurl == None:
                    nurl = ''
                

                #순위 가져오기 
                for c in dblist:
                    if curl != '':
                        ck = curl.find(c[8])
                        if ck != -1:
                            pd_index = c[1]
                            break
                        else:
                            pd_index = 0
                    else:
                        pd_index = 0




                # print('curl===================================',curl)
                if curl =='':    # 쿠팡 url 이 없을 경우 
                    # 네이버 에서 검색   네이버 상품 테이블에서 수집된 데이터 가져옴
                    if nurl !='':  #쿠팡 url은 없으나 nurl 은 있을경우  
                        try:
                            res = requests.get(nurl, headers=self.headers)
                            if res.status_code == 200:
                                soup= bs(res.text,features="lxml")
                                try:
                                    imagepath = soup.select_one('img._2P2SMyOjl6').get('src')
                                    image = imagepath
                                except:
                                    image = 'naver'
                                try:
                                    price = soup.select_one('span._1LY7DqCnwR').get_text()
                                    price = int(price.replace(',','').replace('원',''))
                                except:
                                    price = 0
                                try:
                                    count = soup.select_one('div._2Q0vrZJNK1 a strong._2pgHN-ntx6').get_text()
                                except:
                                    count = 0
                                pd_manager = item[1]
                                pd_code = item[2]
                                titleqs= mqs.filter(pd_code__icontains=pd_code)
                                title = titleqs[0].pd_name
                                state = 'naver'
                                grade = 'naver'
                                url = nurl
                                item = [pd_manager, pd_code, title, state ,count, price, grade,url, image]
                                full_list.append(item)
                                ProductState(id=id,pd_manager =pd_manager, pd_code = pd_code, pd_name = title, pd_state = state, pd_review_count = count , pd_price = price, pd_grade = grade, 
                                pd_image = image,pd_url = url, pd_index = pd_index,mall_name = mall_name ).save()
                                continue
                        except:
                            pass
                        
                    else:
                        pd_manager = item[1]
                        pd_code = item[2]
                        titleqs= mqs.filter(pd_code__icontains=pd_code)
                        title = titleqs[0].pd_name
                        price = 0
                        count = 0
                        state = 'url없음'
                        image = 'url없음'
                        grade = 'url없음'
                        url = 'url없음'
                        item = [pd_manager, pd_code, title, state ,count, price, grade,url, image]
                        full_list.append(item)
                        ProductState(id=id,pd_manager =pd_manager, pd_code = pd_code, pd_name = title, pd_state = state, pd_review_count = count , pd_price = price, pd_grade = grade, 
                        pd_image = image,pd_url = url, pd_index = pd_index,mall_name = mall_name ).save()
                        continue
                else:    # 쿠팡 url이 있을경우 
                    res = requests.get(curl, headers=self.headers)
                    # sleep(1)
                    if res.status_code == 200:
                        soup = bs(res.text,features="lxml")
                        try:
                            #판매중지 체크 
                            out = ''
                            out = soup.select_one('a.prod-not-find-unknown__p').get_text()
                        except:
                            pass
                        # 상품 품절 체크 
                        try:   #쿠팡 에서 품절인지 아닌지 체크 품절일 경우 실행
                            state_Check = soup.select_one('div.oos-label').get_text()
                            ci = -1
                            ci = state_Check.find('일시품절')
                            if ci!=-1:
                                state = '일시품절'
                            pd_manager = item[1]
                            pd_code = item[2]
                            titleqs= mqs.filter(pd_code__icontains=pd_code)
                            title = titleqs[0].pd_name
                            price = 0
                            count = 0
                            percent = soup.select_one('span.rating-star-num').get('style')
                            percent = percent.replace('width: ','').replace('.0%;','')
                            grade = self.grade_change(percent)
                            image = soup.select_one('img.prod-image__detail').get('src')
                            image = 'https:'+image
                            

                            ProductState(id=id,pd_manager =pd_manager, pd_code = pd_code, pd_name = title, pd_state = state, pd_review_count = count , pd_price = price, pd_grade = grade, 
                            pd_image = image,pd_url = curl, pd_index = pd_index,mall_name = mall_name ).save()
                            item = [pd_manager, pd_code, title, state ,count, price, grade, image]
                            full_list.append(item)
                            continue
                        
                        except:  #일시품절이아닐겨우 품절 체크  
                            try:
                                cci = -1
                                state_Check = soup.select_one('div.prod-not-find-known__buy__button').get_text()
                                cci = state_Check.find('품절')
                                if cci != -1:
                                    state = '품절'
                                    pd_manager = item[1]
                                pd_code = item[2]
                                titleqs= mqs.filter(pd_code__icontains=pd_code)
                                title = titleqs[0].pd_name
                                price = 0
                                count = 0
                                percent = soup.select_one('span.rating-star-num').get('style')
                                percent = percent.replace('width: ','').replace('.0%;','')
                                grade = self.grade_change(percent)
                                image = soup.select_one('img.prod-image__detail').get('src')
                                image = 'https:'+image
                            
                                ProductState(id=id,pd_manager =pd_manager, pd_code = pd_code, pd_name = title, pd_state = state, pd_review_count = count , pd_price = price, pd_grade = grade, 
                                pd_image = image, pd_url= curl,pd_index = pd_index,mall_name = mall_name ).save()
                                item = [pd_manager, pd_code, title, state ,count, price, grade, image]
                                full_list.append(item)
                                continue
                            except:  #일시품절 품절이 아닐경우 상품 검색 
                                pass
                        pd_manager = item[1]
                        pd_code = item[2]
                        titleqs= mqs.filter(pd_code__icontains=pd_code)
                        title = titleqs[0].pd_name
                        if out == '':
                            price = soup.select_one('span.total-price strong').get_text().replace(',','').replace('원','')
                            count = soup.select_one('span.count').get_text().replace(',','')
                            if count =='개 상품평':
                                count = 0
                            else:
                                count = count.replace('개 상품평','')
                            image = soup.select_one('img.prod-image__detail').get('src')
                            image = 'https:'+image
                            
                            #평점
                            percent = soup.select_one('span.rating-star-num').get('style')
                            percent = percent.replace('width: ','').replace('.0%;','')
                            grade = self.grade_change(percent)

                            #loket or not loket check not loket is sold out 
                            soldout_check = soup.select_one('td.td-delivery-badge img')
                            if soldout_check:
                                state = '판매중'
                            else:
                                state = '품절'
                        else:
                            price = 0
                            count = 0
                            image = '판매중지'
                            grade = '판매중지'
                            state = '판매중지'

                        # state  0 = 판매중 1 = 일시품절 2 = 품절 3= 품절  (로켓배송이아닐경우 품절 )
                        ProductState(id=id,pd_manager =pd_manager, pd_code = pd_code, pd_name = title, pd_state = state, pd_review_count = count , pd_price = price, pd_grade = grade, 
                        pd_image = image , pd_url = curl ,pd_index = pd_index,mall_name = mall_name).save()
                        item = [pd_manager, pd_code, title, state ,count, price, grade, image]
                        full_list.append(item)
            
        
        return full_list


    def item_review(self):
        # review search  lifingparadiseProduct + ordercompany 3
        if self.dbstate == 'success':
            allqs = Cp_review.objects.all()
        
        
        error_cnt = 0
        pid_list = []
        passCnt = 0
        newReviewCount = 0      #new review count
        todayItem=[]
        todayqs = Cp_c_Product.objects.all()

        todayqs = todayqs.filter(date_info__icontains=self.today)
        for t in todayqs.values_list():
            todayItem.append(t)

        for i in todayItem:
            productId = i[9]
            size = i[11]
            item_id = i[13]
            pid_list.append([productId,size,item_id])



        myitemreview =[]
        rvqs = ProductState.objects.all()
        rmqs = ProductMaster.objects.all()
        for s in rvqs.values_list():
            myitemreview.append(s)  

        for i in myitemreview:
            pd_code = i[2]
            rt = rmqs.filter(pd_code__icontains=pd_code)
            productId = rt[0].cp_code
            size = i[5]
            pid_list.append([productId,size])
        
        #중복된 상품 아아디 제거 
        df = pd.DataFrame(pid_list, columns=['상품아이디','개수','아이템아이디'])
        df= df.drop_duplicates(['상품아이디'])
        pid_list = df.values.tolist()
        sls = len(pid_list)
        i = 0
        
        for i in tqdm(range(0, sls,1), position=0, desc='review crawling'):
            pid = pid_list[i][0]
            size = pid_list[i][1]
            # item_id = pid_list[i][2]
            page = int(size)//100
            page = page+1
            if page > 30:
                page = 30
            #reviewImg saving file create 
            #         path = 'C:/img/'+pid+'/'
    #         if not os.path.isdir(path) :
    #             os.mkdir(path)
            ci = 1
            for ci in range(ci,int(page)+1):
                url = self.review_base_url.format(pid,ci)
                res = requests.get(url, headers=self.headers)
                if res.status_code == 200:
                    soup = bs(res.text,features="lxml")
                    rv_list = []
                    rv_list = soup.select('article.sdp-review__article__list')
    #                 img_list = soup.select('div.sdp-review__article__list__attachment__list')   <<<<<<<<<<<<  review img
                    for review in rv_list:
                        userName = review.select_one('span.sdp-review__article__list__info__user__name').text.strip() 
                        date = review.select_one('div.sdp-review__article__list__info__product-info__reg-date').text.strip()
                        name = review.select_one('div.sdp-review__article__list__info__product-info__name').text.strip()
                        score = review.select_one('div.js_reviewArticleRatingValue').get('data-rating')
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
                        reviewContent = headline + content
                        reviewContent=reviewContent.replace("[^0-9 가-힣 a-z A-Z ]", "")
                        if reviewContent != "":
                            ckRiview = []
                            checkdate = date.replace('.','-')
                            if self.dbstate == 'success':
                                ckRiview =  allqs.filter(product_id__icontains=pid,user_name__icontains=userName,title__icontains=name, date__icontains=checkdate, review__icontains=reviewContent)
                            if ckRiview:
                                break
                            else:
                                self.review_list.append([pid,userName,date,score,name,reviewContent])
                            
                            if self.dbstate == 'success':
                                try:
                                    Cp_review(product_id =pid, user_name = userName, date = date,grade = score, title = name,
                                        review = reviewContent).save()
                                except:
                                    passCnt = passCnt +1
                                    pass
                        #   img save >>>>>
                        # for img in img_list:
                        #    imgpath = img.select_one('img').get('src')
                        #    print(imgpath)
                        #    urllib.request.urlretrieve(imgpath,'C:/img/'+pid+'/'+str(count) + '.jpg')
                    ci=ci+1
        newReviewCount = len(self.review_list)
        

        if self.dbstate == 'success':
            filename = 'ProductReviewResult_{}.csv'.format(self.today)
            filepath ='C:/Croling/living_paradise/Coupang/'+ filename                    
            df = pd.DataFrame(self.review_list, columns=['상품아이디','작성자','작성일','평점','상품명','리뷰'])
            df.to_csv(filepath, index=False, encoding='utf-8')   
        else:
            filename = 'review_{}.csv'.format(self.today)
            filepath = 'C:/Croling/living_paradise/Coupang/db_down_backup/'+ filename                     
            df = pd.DataFrame(self.review_list, columns=['상품아이디','작성자','작성일','평점','상품명','리뷰'])
            df.to_csv(filepath, index=False, encoding='utf-8')   

        insertCnt = newReviewCount - passCnt
        print("new  review searching " , newReviewCount, )
        print("save failed ", passCnt, )
        print("save succes : " , insertCnt, )
        
        if newReviewCount <= 30:
            print(self.review_list)
        
        return self.review_list

   




        #쿠팡 사진 업데이트
    # def imgUpdate(self):
    #     qs = ProductMaster.objects.all()

    #     for s in qs:
    #         if s.cp_url == None:
    #             s.cp_url = ''
    #         if s.cp_url !='':
    #             res = requests.get(s.cp_url, headers=self.headers)
    #             if res.status_code == 200:
    #                 soup = bs(res.text,features="lxml")
    #                 imagepath = soup.select_one('img.prod-image__detail').get('src')
    #                 imagepath = 'https:'+imagepath
    #                 s.image = imagepath
    #                 s.save()
    #                 print(imagepath)
        #네이버 사진 업데이트
    # def imgUpdate(self):
    #     qs = ProductMaster.objects.all()
        
    #     for s in qs:
    #         if s.nv_url == None:
    #             s.nv_url == ''
    #         # print(s.image)
    #         if s.image == None:
    #             if s.nv_url != '':
    #                 try:
    #                     res = requests.get(s.nv_url, headers=self.headers)
    #                     if res.status_code == 200:
    #                         soup= bs(res.text,features="lxml")
    #                         imagepath = soup.select_one('img._2P2SMyOjl6').get('src')
    #                         s.image = imagepath
    #                         s.save()
    #                         # print(s.id)
    #                         # print(imagepath)
    #                 except:
    #                     pass

    # 쿠팡 코드 업데이트
    # def c_code_update(self):
    #     qs = ProductMaster.objects.all()

    #     for s in qs:
    #         if s.cp_url == None:
    #             s.cp_url = ''
    #         if s.cp_url != '':
    #             # https://www.coupang.com/vp/products/99504?itemId=11395882
    #             first = s.cp_url.find('products/')+9
    #             last = s.cp_url.find('?itemId=')
    #             if last == -1:
    #                 last = s.cp_url.find('?vendorItemId=')
    #             cp_code = s.cp_url[first:last]
    #             print(cp_code)
    #             s.cp_code = cp_code
    #             s.save()   
    
    
    
    
    
    
    
    def test(self):
        myitem_list = []
        qs = Cp_c_Product.objects.all()
        for s in qs.values_list():
            myitem_list.append(s)
        df = pd.DataFrame(myitem_list, columns=['ID','PD_INDEX','CHANGE_INDEX','COMPANY','KEYWORD','TITLE','STATE','PAGE_LINK','PRODUCT_ID','PRICE','REVIEW_COUNT','IMAGE_LINK'
        ,'ITEM_ID','GRADE','DATE_INFO'])
        ts = df.to_dict('records')
        print(ts[1])

        # 제이슨 파일 로 저장 하기 
        with open('.COUPANGPRODUCT.json','w', encoding='utf-8') as f:
            json.dump(ts, f, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)    # cls  => 날짜 형식 타입 에러 나는걸 막기위한 django 모듈 사용

        
















        
        

             

    
    


    
# self.noAD_list.append([keyword,item_num,item_name, link,pid, price,review_count,image_path,vendor_itemId,score])
    # def item_average(self):
            
    #     s = 0
    #     pid_list = []
    #     for i in self.noAD_list:
    #         productId = self.noAD_list[s][4]
    #         itemId = self.noAD_list[s][8]
    #         itemName = self.noAD_list[s][2]
    #         pid_list.append(productId,itemId, itemName)
    #         s=s+1
    #     percent_list = []
    #     average_summary_list= []
    #     average_list=[]
    #     i = 0
    #     base_url = 'https://www.coupang.com/vp/product/reviews/summaries?productId={}'
    #     headers = {
    #         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'    
    #     }
    #     for pid in pid_list:
    #         url = base_url.format(pid[0])
    # #      테스트용   print(url)
    #         res = requests.get(url, headers=headers)
    #         if res.status_code == 200:
    #             soup = bs(res.text)
    #             try:
    #                 score = soup.select_one('div.js_reviewAverageTotalStarRating').get('data-rating')
    #             except:
    #                 score = '0'
    #             try:
    #                 reviewCount = soup.select_one('div.sdp-review__average__total-star__summary__total__count').text.strip()
    #             except:
    #                 reviewCount = '리뷰가 없습니다.'
    #             summary_list = soup.select('div.sdp-review__average__total-star__summary__graph')
    #             percent_list = []
    #             average_summary_list= []
    #             for summary in summary_list:
    #                 sname = summary.select_one('div.sdp-review__average__total-star__summary__graph__state').text.strip()
    #                 percent = summary.select_one('div.sdp-review__average__total-star__summary__graph__percent').get_text()
    #                 percentlist = sname + percent
    #                 percent_list.append(percentlist)
    #             percent_list = " ".join(map(str,percent_list))
    #             ast_list = soup.select('section.sdp-review__average__summary__section')
    #             ass_list = soup.select('li.sdp-review__average__summary__section__list__item')
    #             #타이틀 뽑아내서 타이틀 리스트 만들기
    #             try:
    #                 title = soup.select('header.sdp-review__average__summary__section__title')
    #                 title_list = []
    #                 for ts in title:
    #                     ton = ts.get_text()
    #                     title_list.append(ton)
    #             except:
    #                 title_list = [" "," "," "]
    #             for asl in ass_list:
    #                 average_summary=""
    #                 try:
    #                         perc= asl.select_one('div.sdp-review__average__summary__section__list__item__graph__percent').get_text()
    #                 except:
    #                         perc= '0%'
    #                 percname= asl.select_one('div.sdp-review__average__summary__section__list__item__answer').get_text()
    #                 average_summary =  perc + percname
    #                 if average_summary!="":
    #                     average_summary_list.append(average_summary)
    #             if len(average_summary_list)==9:  
    #                 average_summary_list.insert(0,"  "+title_list[0]+" : ")
    #                 average_summary_list.insert(4,"  "+title_list[1]+" : ")
    #                 average_summary_list.insert(8,"  "+title_list[2]+" : ")
    #             elif len(average_summary_list)==3:  
    #                 average_summary_list.insert(0,"  "+title_list[0]+" : ")
    #             elif len(average_summary_list)==6:  
    #                 average_summary_list.insert(0,"  "+title_list[0]+" : ")
    #                 average_summary_list.insert(4,"  "+title_list[1]+" : ")
    #             average_summary_list = " ".join(map(str,average_summary_list))
    #             if reviewCount != '리뷰가 없습니다.':
    #                 average_list.append([pid[2],pid[0],pid[1], score, reviewCount,percent_list,average_summary_list])

    #             i= i+1
    #     df = pd.DataFrame(average_list, columns=['제품명','제품ID','itemID','점수','리뷰개수','에버리지','만족도'])




    

        # cc.imgUpdate()
        # cc.test()