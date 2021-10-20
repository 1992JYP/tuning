## 작성 2021-06-22  - 이유인 
## 수정  2021- 08-31  - 이유인

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
from datetime import datetime,timedelta
import re
import os
import pandas as pd
from .models import Cp_c_Product , Cp_review
from tqdm import tqdm



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

        self.today = datetime.now()
        self.yesterday = self.today- timedelta(1)
        self.today = self.today.strftime("%Y-%m-%d")
        self.yesterday = self.yesterday.strftime("%Y-%m-%d")
        try:
            self.yesterdf = pd.read_excel(io='C:/Croling/상품정보조회결과_'+self.yesterday+'.xlsx', sheet_name='Sheet1')
        except:
            self.yesterdf = self.productDF = pd.DataFrame(columns=['키워드','상품랭킹','아이템순위변동','제조사','상품명','판매상태','상품링크','상품아이디','가격','리뷰개수','이미지링크','아이템아이디','평점'])
        # soup 사용시 heards
        self.headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'    
            }
        #
        self.item_search_base_url = 'https://www.coupang.com/np/search?q={}&page={}'
        self.review_base_url = 'https://www.coupang.com/vp/product/reviews?productId={}&page={}&size=100&sortBy=DATE_DESC'



    def search_listup(self):
        try:
            df = pd.read_excel(io='C:/Croling/'+self.excelfile_name, sheet_name=self.excelsheet_name)
            df = df.dropna(subset=['쿠팡URL','매칭키워드'])  #결측치 제거
            matchingKeyword = df['매칭키워드']
            matchingKeyword = matchingKeyword.drop_duplicates()  #중복제거
            matchingKeyword=matchingKeyword.values.tolist()
            url_list = df['쿠팡URL']
            url_list = url_list.values.tolist()
            self.df = df.values.tolist()

            # url_list = df.values.tolist()
            #검색 키워드 리스트 뽑기
            
            for item in matchingKeyword:
                self.keyword_list.append(item)
            #체크 url 리스트
            for item in url_list:
                last_index = item.find('&q=')
                self.ck_url_list.append(item[:last_index])
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
            for page in range(1,int(last_page)+1):        # 전체 상품 크롤링시  위의 last_page 활용 하여 돌리기  int(last_page)+2
                # if  item_check_num == self.lastItemCheck:    # 아이템 10개씩만 가져오기위해 넣은 조건문 제한 없을시 제거 
                #     break                                           
                #자회사 제품 전부와 다른회사 제품 3개 크롤링 완료시 다음 키워드로
                if itemcount==myitemCheck and otherCheck==3:
                            break                    
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
                                state = 1
                            else:
                                state = 2    
                        except:
                            state = 0
                        try:
                            vendor_itemId = item.select_one('a').get('data-vendor-item-id')
                            item_name = item.select_one('div.name').text.strip()
                            link = item.select_one('a').get('href')
                            link = parse.urljoin(cp_url, link)
                            # 링크 비교 
                            for url in self.ck_url_list:
                                if url==link:
                                    checkbool = True
                                    company = 0
                                    break
                                else:
                                    checkbool = False
                                    company = 1
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
                                self.noAD_list.append([keyword,item_num,change_index,company,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score])  #광고를 제회한 전체 리스트목록
                                

                                if checkbool:
                                    self.myItem.append([keyword,item_num,change_index,company,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score])  #생활낙원 제품 목록
                                    self.sumItem.append([keyword,item_num,change_index,company,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score])
                                    Cp_c_Product(keyword =keyword, pd_index = item_num,change_index = change_index, company = company, state = state, title = item_name, page_link = link,
                                            product_id = pid, price = price, review_count = review_count,
                                            image_link = image_path, item_id = vendor_itemId, grade = score).save()
                                    myitemCheck = myitemCheck+1
                                    print('생확낙원 제품 save', myitemCheck,'/',itemcount)
                                else:
                                    self.otheritem.append([keyword,item_num,change_index,company,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score])
                                    
                                    if otherCheck <3:
                                        self.sumItem.append([keyword,item_num,change_index,company,item_name,state, link,pid, price,review_count,image_path,vendor_itemId,score])
                                        Cp_c_Product(keyword =keyword, pd_index = item_num,change_index = change_index, company = company, state = state, title = item_name, page_link = link,
                                                product_id = pid, price = price, review_count = review_count,
                                                image_link = image_path, item_id = vendor_itemId, grade = score).save()
                                       
                                        otherCheck = otherCheck+1
                                        print('다른회사제품 save', otherCheck, '  개')
                            # self.result_list.append([keyword, allItemNum,item_name, link,pid, price,review_count,image_path,vendor_itemId,score])  #광고 포함 총 목록
                            allItemNum = allItemNum+1
                        except:
                            error_cnt+1
        
        filename = '상품정보조회결과_{}.xlsx'.format(self.today)
        filepath ='C:/Croling/'+ filename                    
        df = pd.DataFrame(self.noAD_list, columns=['키워드','상품랭킹','아이템순위변동','제조사','상품명','판매상태','상품링크','상품아이디','가격','리뷰개수','이미지링크','아이템아이디','평점'])
        df.to_excel(filepath, index=False, encoding='utf-8')                   
        print('광고 포함 총 상품 개수 : ' , allItemNum ,' 개')
        print('광고 제거  총 상품 개수 : ' ,noAddNum ,' 개')
        print('생활낙원  총 상품 개수 : ' ,len(self.myItem) ,' 개')

        print('생활낙원  총 상품 개수 : ' ,len(self.myItem) ,' 개')
        return self.sumItem    

    def item_review(self):
        # 리뷰 검색 생활낙원제품 + 경쟁사 3
        error_cnt = 0
        s = 0
        pid_list = []
        passCnt = 0
        newReviewCount = 0      #새로운 리뷰개수
        for i in self.sumItem:
            productId = self.sumItem[s][7]
            size = self.sumItem[s][9]
            item_id = self.sumItem[s][11]
            pid_list.append([productId,size,item_id])
            s=s+1
        #중복된 상품 아아디 제거 
        df = pd.DataFrame(pid_list, columns=['상품아이디','개수','아이템아이디'])
        df= df.drop_duplicates(['상품아이디'])
        pid_list = df.values.tolist()
        sls = len(pid_list)
        i = 0
        
        for i in tqdm(range(0, sls,1), position=0, desc='상품리뷰 크롤링'):
            pid = pid_list[i][0]
            size = pid_list[i][1]
            item_id = pid_list[i][2]
            page = int(size)//100
            page = page+1
            if page > 30:
                page = 30
            #리류이미지 담을 폴더 생성 
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
    #                 img_list = soup.select('div.sdp-review__article__list__attachment__list')   리뷰이미지
                    for review in rv_list:
                        userName = review.select_one('span.sdp-review__article__list__info__user__name').text.strip() 
                        date = review.select_one('div.sdp-review__article__list__info__product-info__reg-date').text.strip()
                        name = review.select_one('div.sdp-review__article__list__info__product-info__name').text.strip()
                        score = review.select_one('div.js_reviewArticleRatingValue').get('data-rating')
                        headline = review.select_one('div.sdp-review__article__list__headline')  
                        #텍스트를 가져오려할시 error  태크채로 가져와 str 치환후 정규 표현식 사용 태그 벗김
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
                        if reviewContent != "":
                            ckRiview = []
                            checkdate = date.replace('.','-')
                            qs = Cp_review.objects.all()
                            ckRiview =  qs.filter(product_id__icontains=pid,user_name__icontains=userName,title__icontains=name, date__icontains=checkdate, review__icontains=reviewContent)
                            if ckRiview:
                                break
                            else:
                                self.review_list.append([pid,userName,date,score,name,reviewContent])
                            try:
                                Cp_review(product_id =pid, user_name = userName, date = date,grade = score, title = name,
                                     review = reviewContent).save()
                            except:
                                passCnt = passCnt +1
                                pass
                        #    이미지 저장시 
                        # for img in img_list:
                        #    imgpath = img.select_one('img').get('src')
                        #    print(imgpath)
                        #    urllib.request.urlretrieve(imgpath,'C:/img/'+pid+'/'+str(count) + '.jpg')
                    ci=ci+1
        newReviewCount = len(self.review_list)
        insertCnt = newReviewCount - passCnt
        print("새로운  리뷰 검색수 " , newReviewCount, " 개")

        print("save failed ", passCnt, " 개")
        print("save succes : " , insertCnt," 개" )
        
        if newReviewCount <= 50:
            print(self.review_list)
        
        return self.review_list

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


