from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView

from django.views import View
from apps.paradise import models as lpmodels
from apps.main import models
from apps.main.models import NvProduct
from apps.main.models import NvReview

from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.alert import Alert
from openpyxl import load_workbook
import chromedriver_autoinstaller
import operator

class naverCrawler:
    def url_start1(self): # 1번
        # 원본 파일 경로 넣어
        original_excel = pd.read_excel('C:/Users/user/Desktop/코스메카코리아 + 생활낙원/매칭키워드_정리_URL 매칭.xlsx')

        self.want_it_excel = original_excel[['품목코드','품목명','매칭키워드','네이버URL']]
        
        my_urls = self.want_it_excel[['네이버URL']] # 본 컬럼의 인덱스만 가져와서 담음

        urls_list = my_urls.values.tolist() # DF를 리스트로 바꿈

        self.my_url_len = len(my_urls) # 인덱스의 총 개수, 935개있음
        
        self.want_it_excel.insert(0, 'rank', '') # 랭크킹 0번째 그러니깐 제일 앞에 저거 한줄 만든다고
        
        this_my_excel = self.want_it_excel[['rank','품목코드','매칭키워드']]
        
        # 새로운 컬럼을 만들고
        this_my_excel[['title', 'price', 'review_count', 'serial_number', 'prod', 'link', 'score_avg', 'image','item_states']] = ''
         
        # 만들어진걸 추가하고
        self.cook_it_this = this_my_excel[['rank','품목코드','매칭키워드','title', 'price', 'review_count', 'serial_number', 'prod', 'link', 'score_avg', 'image','item_states']]
        #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        self.come_url = 0 # url 위치 파악용
        self.first_do_it = 1 # 본사 상품 정보 긁을때 쓰는거, 최초 1회만 되면 됨

        #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

        for url_list in urls_list:
            for url in url_list:
                type_this = str(url) # 문자형으로 다 바꿔
                if type_this != 'nan': # 결측기가 아니면 들가
                    self.options = wb.ChromeOptions()
                    self.options.add_argument('headless')
                    self.options.add_argument('window-size=1920x1080')
                    self.options.add_argument("disable-gpu")

                    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

                    try:
                        self.driver =  wb.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options = self.options)   
                    except:
                        chromedriver_autoinstaller.install(True)
                        self.driver =  wb.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options = self.options)

                    self.driver.get(url)
                    time.sleep(0.5)
                    # = = = = = start
                    try:
                        have_u_item = self.driver.find_element_by_css_selector('#content > div > div > strong._141KVzmWyN').text
                        self.cook_it_this.loc[self.come_url,['item_states']] = have_u_item
#                         self.where_is_it()
                        self.driver.close()
                    except:
                        try:
                            stop_selling = self.driver.find_element_by_css_selector('#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._2BQ-WF2QUb > strong').text
                            if stop_selling == '이 상품은 현재 구매하실 수 없는 상품입니다.':
                                self.cook_it_this.loc[self.come_url,['item_states']] = stop_selling
                                self.where_is_it()
                            else:
                                self.cook_it_this.loc[self.come_url,['item_states']] = stop_selling
#                                 self.where_is_it()
                                self.driver.close()
                        except:
                            self.where_is_it() #긁을게 있어야 들어가는거야 여기는
                            self.driver.close()
                        time.sleep(1)

                else: # 결측지면 들어가
                    self.cook_it_this.loc[self.come_url,['link']] = 'url없음'
                    

                self.first_do_it += 1 # 전체935개를 url이 있냐 없냐로 나뉘어 들어가기때문에 이거 저거 다끝나고 공통이로 먹어야함

                self.come_url += 1
    
        if self.first_do_it >= self.my_url_len: # 본사 상품정보를 다 긁어서 DB에다가 담게 되면 이제 랭킹과 타사 상품 정보 긁으러 들거간다

            self.url_start2()

            
                

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def url_start2(self): # 4번
        url = 'https://shopping.naver.com/'
        self.options = wb.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")

        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

        try:
            self.driver =  wb.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options = self.options)   
        except:
            chromedriver_autoinstaller.install(True)
            self.driver =  wb.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options = self.options)

        self.driver.get(url)
        
        #======================================================================================================
        
        # 변수
        self.while_count = 0 # while 반복문 제어
        self.othercheck = 1 # 타사체크
        
        self.this_tem_number = 0 # 상품 태그 페이징
        self.index_number = 0 # 상품 인덱스에 붙는거
        
        self.re_next_num = 3 # 리뷰 태그 페이징
        self.re_index = 0 # 리뷰 인덱스에 붙는거
        
        self.rank_num = 0 # 본사 랭크 재려고 만든거(한번만 쓰고 안쓸거야)
        
        self.all_count = 0 # 이것의 쓰임은 본사제품이 10개 모였냐 확인하려 만든거야
#         self.reviewDF = pd.DataFrame(columns=['index', 'serial_number', 'text', 'score', 'option','review_date'])
        self.reviewDF = pd.DataFrame(columns=['product_id', 'user_name', 'date', 'grade', 'title', 'review', 'option'])
        #======================================================================================================
        
        matching_keywords = self.want_it_excel[['매칭키워드']] # 본 컬럼의 인덱스만 가져와서 담음 , 키워드
        keyword_deduplication = matching_keywords.drop_duplicates() # 키워드속 중복 제거
        matching_keyword = keyword_deduplication[keyword_deduplication.index.notnull()]
        matching_key = matching_keyword.dropna(how='all')  # 공백 제거, 격측치값 제거
        self.matching_word = matching_key.values.tolist()    # 데이터프레임을 리스트화
        self.matching_word_one = keyword_deduplication.values.tolist()    # 데이터프레임을 리스트화        
        
        self.find_keyword = [] # 데프안의 타이틀명만 담을라고 
        
        for it_keywords in self.matching_word_one:
            self.find_keyword.append(it_keywords[0])
        
        # 본사 인덱스에 기록하기위한것들_________
        matching_keyword_list = matching_keywords.values.tolist() 
        
        self.matching_keyword_lists =[]

        for matching_keyword_one in matching_keyword_list:
            self.matching_keyword_lists.append(matching_keyword_one[0])
                
        #======================================================================================================
        
        matching_titles = self.cook_it_this[['title']] # 본 컬럼의 인덱스만 가져와서 담음 , 본사상품명
        title_deduplication = matching_titles.drop_duplicates() # 키워드속 중복 제거
        matching_title = title_deduplication[title_deduplication.index.notnull()]
        matching_tit = matching_title.dropna(how='all')    # 공백제거, 데이터프레임속 결측치 제거
        matching_t = matching_tit.values.tolist()    # 데이터프레임을 리스트화
        
        self.find_title = [] # DF안의 타이틀명만 담을라고 
        
        for it_titles in matching_t:
            for it_title in it_titles:
                self.find_title.append(it_title)
        
        matching_titles_list = matching_titles.values.tolist() 
        # title불러온걸 리스트로 만들면 935개 들어있는 전체가 나옴
        self.find_titles = []
        
        for find_it_titles in matching_titles_list:
            for find_it_title in find_it_titles:
                self.find_titles.append(find_it_title)
        #====================================================================================================== 
        self.find_urls = self.cook_it_this[['link']] # 여기서 가져오면 네이버url속에는 앞전에 데이터 긁은대로 들어있음
        find_url_lists = self.find_urls.values.tolist() # 그렇게 된걸 url로  바꿈
        
        self.this_url_list = []
        
        for find_url_list in find_url_lists:
            for find_url in find_url_list:
                self.this_url_list.append(find_url)
        #====================================================================================================== 
        item_states = self.cook_it_this[['item_states']]
        find_item_states = item_states.values.tolist()  # 상품 상태
        
        self.this_item_state_list = []
        
        for find_item_state in find_item_states:
            for find_state in find_item_state:
                self.this_item_state_list.append(find_state)
        #====================================================================================================== 
        
            
        self.fcrawgo()
# = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def smart(self): # 3번 7번

        html = self.driver.page_source 
        soup_item = BeautifulSoup(html, "html.parser")
        smart_item_info = soup_item.select_one('div._2ZMO1PVXbA')

        th = self.driver.find_elements_by_css_selector('table > tbody > tr > th._1iuv6pLHMD')
        td = self.driver.find_elements_by_css_selector('table > tbody > tr > td.ABROiEshTD')

        dictkey = []
        dictvalue = []

        for ths in th:
            dictkey.append(ths.text)
        for tds in td:
            dictvalue.append(tds.text)

        # key값 상품번호 / 상품상태 / 제조사 / 브랜드 / 모델명 / 이벤트 / 사음품 / 원산지
        tables = dict(zip(dictkey, dictvalue))

        link = self.driver.current_url

        title = smart_item_info.select_one('h3').text
        print(f'title >> {title}')

        try:
            self.serial_number = tables['상품번호'].replace('<b>','')
        except:
            self.serial_number = link[47:58]
        print(f'serial_number >> {self.serial_number}')

        price = smart_item_info.select_one('span._1LY7DqCnwR').text.replace(',','')
        print(f'price >> {price}')

        review_count = smart_item_info.select_one('strong._2pgHN-ntx6').text.replace(',','')
        print(f'review_count >> {review_count}')

        score_avg = smart_item_info.select_one('div._2Q0vrZJNK1 > strong._2pgHN-ntx6').text.replace('/5','')
        print(f'score_avg >> {score_avg}')

        image = smart_item_info.select_one('img').get('src')
        print(f'image >> {image}')


        print(f'link >> {link}')

        try:
            prod = tables['제조사']
        except:
            prod = None
        print(f'prod >> {prod}')

        try:
            item_states = self.driver.find_element_by_css_selector('#content > div > div > strong._141KVzmWyN').text
        except:
            try:
                item_states = self.driver.find_element_by_css_selector('#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._2BQ-WF2QUb > strong').text
            except:
                item_states = None
        print(f'item_states >> {item_states}')

        try:
            self.rank = self.rank_num
        except:
            self.rank = ''
            
        # 긁어서 담고
        self.smart_item_infor = [self.rank, title, price, review_count, self.serial_number, prod, link, score_avg, image, item_states]
        
        #담은거 넣고, self.come_url 번째 인덱스에 들어감 본사상품 총 935개 이후 타사제품 들어감
        self.cook_it_this.loc[self.come_url,['rank', 'title', 'price', 'review_count', 'serial_number', 'prod', 'link', 'score_avg', 'image', 'item_states']] = self.smart_item_infor
        # df에 담아 넣었다 여기까지가
#======================================================================================================
    def smart_review(self): # 8번
        self.re_index += 1
        
        for i in range(2): # 스크롤내리기
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.3)
            
        try:
            # 한 페이지당 보여지는 리뷰갯수 20개
            review_tag_len = len(self.driver.find_elements_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul > li'))
            print('review_tag_len >> {}'.format(review_tag_len))
        except:
            pass
        
        try:
            # 페이징을 한장씩 할거니까 거 갯수 제한걸려 만든거
            smart_items_num = int(self.driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > strong > span').text.replace('(','').replace(')','').replace(',',''))
            in_number = round(smart_items_num / review_tag_len)
            if in_number > 100: #리뷰 최대가 2000개라 
                in_number = 99
            print(f'in_number >> {in_number}')
        except:
            pass
        
        link = self.driver.current_url
        self.smart_serial_number = link[47:58].replace('/','')
        
        try:
            item_title = self.driver.find_element_by_css_selector('#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1ziwSSdAv8 > div.CxNYUPvHfB > h3').text
            print(f'item_title >> {item_title}')
            
            # 최신버튼
            self.driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a').send_keys(Keys.ENTER)

            for index in range(in_number): # 페이징 태그갯수

                html = self.driver.page_source
                soup_item = BeautifulSoup(html, "html.parser")
                smart_items = soup_item.select_one('ul.TsOLil1PRz')

                for smart_item in smart_items:
                    
                    text = smart_item.select_one('div.YEtwtZFLDz > span._3QDEeS6NLn').text
                    print(f'text >> {text}')

                    score = smart_item.select_one('div._2V6vMO_iLm > em._15NU42F3kT').text
                    print(f'score >> {score}')
                    try:
                        option = smart_item.select_one('button._3jZQShkMWY > span._3QDEeS6NLn').text
                    except:
                        option = None
                    print(f'option >> {option}')

                    review_date = smart_item.select_one('div._2FmJXrTVEX > span._3QDEeS6NLn').text
                    print(f'review_date >> {review_date}')
                    
                    user_name = smart_item.select_one('strong._3QDEeS6NLn').text
                    print(f'user_name >> {user_name}')


                    NvReview(
                    PRODUCT_ID = self.smart_serial_number,
                    USER_NAME = user_name,
                    DATE = review_date,
                    GRADE = score,
                    TITLE = item_title,
                    REVIEW = text,
                    P_OPTION = option,
                    ).save()


                     #리뷰 담는거
                    # 이거 한줄씩 담는거잖아 앞에서 만들어 놓은 self.reviewDF 안에다가 말이지
                    # 긁어담아
                    self.reviewDF.loc[len(self.reviewDF)] = [self.smart_serial_number, user_name, review_date, score, item_title, text, option]
                print('♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥') 
                time.sleep(1.8)

                try:
                    re_pageing_buton = self.driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a:nth-child(%d)'%self.re_next_num)
                    re_pageing_buton.send_keys(Keys.RETURN)
                    re_pageing_buton_text = re_pageing_buton.text
                    print(f're_pageing_buton_text >> {re_pageing_buton_text}')

                    if re_pageing_buton_text == '다음':
                        self.re_next_num = 3
                    elif re_pageing_buton_text == '100':
                        break
                    else:
                        self.re_next_num += 1
                except:
                    break
        except:
            pass
#======================================================================================================
    def search(self): # 3번 7번

        th = self.driver.find_elements_by_css_selector('#__next > div > div.style_container__3iYev > div.style_inner__1Eo2z > div.top_summary_title__15yAr > div.top_info_inner__1cEYE > span.top_cell__3DnEV')
        td = self.driver.find_elements_by_css_selector('#__next > div > div.style_container__3iYev > div.style_inner__1Eo2z > div.top_summary_title__15yAr > div.top_info_inner__1cEYE > span.top_cell__3DnEV > em')

        search_dictkey = []
        search_dictvalue = []

        for ths in th:
            search_dictkey.append(ths.text)
        for tds in td:
            search_dictvalue.append(tds.text)

        keylist = []
        valuelist =[]
        for dic in search_dictkey:
            for em in search_dictvalue:
                num = dic.find(em)
                if num>-1:
                    keylist.append(dic[:num-1])
                    valuelist.append(em)    

        info_tables = dict(zip(keylist, valuelist))

        html = self.driver.page_source 
        soup_item = BeautifulSoup(html, "html.parser")
        search_item_info1 = soup_item.select_one('div.top_summary_title__15yAr')

        title = search_item_info1.select_one('h2').text
        print(f'title >> {title}')

        html = self.driver.page_source 
        soup_item = BeautifulSoup(html, "html.parser")
        search_item_info2 = soup_item.select_one('div.style_content_wrap__2VTVx')

        link = self.driver.current_url

        self.search_serial_number = link[42:53].replace('?','')
        print(f'search_serial_number >> {self.search_serial_number}') #일단 보류

        price = search_item_info2.select_one('em.lowestPrice_num__3AlQ-').text
        print(f'price >> {price}')
        try:
            review_count = search_item_info2.select_one('li.filter_on__X0_Fb > a > em').text.replace('(','').replace(')','').replace(',','')
        except:
            review_count = '0'
        print(f'review_count >> {review_count}')
        
        try:
            score_avg = search_item_info2.select_one('div.totalArea_value__3UEUi').text.replace('/5','')
        except:
            score_avg = '0'
        print(f'score_avg >> {score_avg}')

        image = search_item_info2.select_one('img').get('src')
        print(f'image >> {image}')

        print(f'link >> {link}')

        try:
            prod = info_tables['제조사']
        except:
            prod = None

        print(f'prod >> {prod}')
        
        item_states = ''
        
        try:
            self.rank = self.rank_num
        except:
            self.rank = ''
            
        # 긁어서 담고
        self.search_item_infor = [self.rank, title, price, review_count, self.search_serial_number, prod, link, score_avg, image, item_states]
        # 담은거 들어가고
        self.cook_it_this.loc[self.come_url,['rank', 'title', 'price', 'review_count', 'serial_number', 'prod', 'link', 'score_avg', 'image', 'item_states']] = self.search_item_infor
       
        self.search_review()
#====================================================================================================== 
    def search_review(self):#  8번
        
        self.re_index += 1
        
        for i in range(2): # 스크롤내리기
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.3)

        try:
            # 한 페이지당 보여지는 리뷰갯수 20개
            review_tag_len = len(self.driver.find_elements_by_css_selector('#section_review > ul > li'))
        except:
            pass

        try:
            # 페이징을 한장씩 할거니까 거 갯수 제한걸려 만든거
            search_items_num = int(self.driver.find_element_by_css_selector('#section_review > div.filter_sort_group__Y8HA1 > div.filter_evaluation_tap__-45pp > ul > li.filter_on__X0_Fb > a > em').text.replace('(','').replace(')','').replace(',',''))
            in_number = round(search_items_num / review_tag_len)
            if in_number > 100: #리뷰 초대가 2000개라 
                in_number = 99
            print(f'in_number >> {in_number}')
        except:
            pass


        try:
            # 최신순
            new_one = self.driver.find_element_by_xpath('//*[@id="section_review"]/div[2]/div[1]/div[1]/a[2]')
            new_one.send_keys(Keys.RETURN)
            new_one.click()
            self.se_next_num = 2
            time.sleep(1.8)
            
            item_title = self.driver.find_element_by_css_selector('#__next > div > div.style_container__3iYev > div.style_inner__1Eo2z > div.top_summary_title__15yAr > h2').text
            print(f'상품명 >> {item_title}')
            
            for index in range(in_number): # 페이징 태그갯수
                html = self.driver.page_source
                soup_item = BeautifulSoup(html, "html.parser")
                seach_items = soup_item.select_one('ul.reviewItems_list_review__1sgcJ')

                for seach_item in seach_items:

                    text = seach_item.select_one('p.reviewItems_text__XIsTc').text.replace('\n','')
                    print('리뷰글 >> {}'.format(text))

                    score = seach_item.select_one('span.reviewItems_average__16Ya-').text.replace('평점','')
                    print('별점 >> {}'.format(score))

                    try:
                        option = seach_item.select_one('div.reviewItems_etc_area__2P8i3 > span:nth-of-type(5)').text
                    except:
                        option = None
                    print(f'option >> {option}')

                    review_date = seach_item.select_one('div.reviewItems_etc_area__2P8i3 > span:nth-of-type(4)').text
                    print('날짜 >> {}'.format(review_date))
                    
                    user_name = seach_item.select_one('div.reviewItems_etc_area__2P8i3 > span:nth-of-type(3)').text
                    print(f'작성자 >> {user_name}')

                    NvReview(
                    PRODUCT_ID = self.serial_number,
                    USER_NAME = user_name,
                    DATE = review_date,
                    GRADE = score,
                    TITLE = item_title,
                    REVIEW = text,
                    P_OPTION = option,
                    ).save()

                    #리뷰 담는거
                    self.reviewDF.loc[len(self.reviewDF)] = [self.search_serial_number, user_name, review_date, score, item_title, text, option]
                time.sleep(1.5)
                print('♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥') 


                try:
                    self.driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 > a:nth-child(%d)'%self.se_next_num).click()
                    review_tag_text = self.driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 > a:nth-child(%d)'%self.se_next_num).text
                    time.sleep(1.5)

                    if review_tag_text == '다음':
                        self.se_next_num = 3
                    elif review_tag_text == '100':
    #                     self.index_num = 0 # 또는 그냥 다 읽고나면 리셋
                        break
                    else:
                        self.se_next_num += 1

                except:
                    break
        except:
            pass
#====================================================================================================== 
    def in_crawling(self): # 6번 
        
        title_url = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a'%self.this_tem_number)
        ## 선택한 제품 클릭  
        title_url.send_keys(Keys.RETURN)
        time.sleep(4)

        ## 제품 선택하고 생성된 새창으로 포커스 이동 
        last_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(window_name = last_tab)
        time.sleep(3)

        ## 해당 url 주소 가져오기 
        input_url = self.driver.current_url

        ## 가져온 주소에서 smartstore.naver.com 있는지 판단  -1 이 있다면 없음 
        naver_shop = input_url.find('smartstore.naver.com') #  주소안에스마트스토어만 찾아서 담아
    #===============================================================================        
        ## 불러온 url  -1 이면 
        if naver_shop == -1:

            naver_shop = input_url.find('search.shopping.naver.com')

            if naver_shop == -1:
                c_type = -1

            else :
                c_type = 2

        else :
            c_type = 1
    #===============================================================================
        
        
        if c_type == 1:
            if self.title in self.find_title: # 본사 유무를 파악해서 맞으면 들어가 리뷰를 긁을거임
                self.smart_review()
            else:                             # 틀리면 타사기때문에 상품정보와 1초쉬고 리뷰를 긁을거임
                self.smart()
                insertlist = list(self.cook_it_this.iloc[[self.come_url][0]]) # 타사 상품정보도 긁었으니 한줄 담아야지?
                time.sleep(1)
                self.smart_review()
                
            # csv로 저장
            self.reviewDF.to_csv(f'naver_review_{self.re_index}.csv', index = False, encoding = 'utf-8')
            
            # 방금 저장 했지? self.smart_serial_number 변수명에 해당하는것들 다 지워놔
            self.reviewDF = self.reviewDF.drop(index = self.reviewDF.loc[self.reviewDF.product_id == self.smart_serial_number].index)
            print('스마트_둘다 함?')

#이건 db에 담는거라 상관없어 
            NvProduct(
            rank_num = insertlist[0],
            item_code = insertlist[1],
            keyword = insertlist[2],
            title = insertlist[3],
            price = insertlist[4].replace(',',''),
            review_count = insertlist[5],
            serial_number = insertlist[6],
            prod = insertlist[7],
            link = insertlist[8],
            score_avg = insertlist[9],
            image = insertlist[10],
            item_states = insertlist[11]
            ).save()

            self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)

            

        elif c_type == 2:
            try:
                self.driver.find_element_by_css_selector('#__next > div > div.style_content_error__3Wxxj > p.style_desc__1jrM5')
                # 새로고침
                self.driver.get(self.driver.current_url)
            except:
                pass
            
            self.search()
            
            insertlist = list(self.cook_it_this.iloc[[self.come_url][0]])
            
            # csv로 저장
            self.reviewDF.to_csv(f'naver_review_{self.re_index}.csv', index = False, encoding = 'utf-8')
            # 방금 저장 했지? self.search_serial_number 변수명에 해당하는것들 다 지워놔
            self.reviewDF = self.reviewDF.drop(index = self.reviewDF.loc[self.reviewDF.product_id == self.search_serial_number].index)
            print('서치_둘다 함?')

            
#이거살려            
            NvProduct(
            rank_num = insertlist[0],
            item_code = insertlist[1],
            keyword = insertlist[2],
            title = insertlist[3],
            price = insertlist[4].replace(',',''),
            review_count = insertlist[5],
            serial_number = insertlist[6],
            prod = insertlist[7],
            link = insertlist[8],
            score_avg = insertlist[9],
            image = insertlist[10],
            item_states = insertlist[11]
            ).save()

            self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)

            
        else:
            self.driver.close()
            # 팝업 창 닫기 
            if len(self.driver.window_handles) >1:
                last_tab = self.driver.window_handles[1]
                self.driver.switch_to.window(window_name=last_tab)
                self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)
            
#====================================================================================================== 

    def where_is_it(self): # 2번 
        ## 해당 url 주소 가져오기 
        input_url = self.driver.current_url

        ## 가져온 주소에서 smartstore.naver.com 있는지 판단  -1 이 있다면 없음 
        naver_shop = input_url.find('smartstore.naver.com') #  주소안에스마트스토어만 찾아서 담아
        #===============================================================================        
        ## 불러온 url  -1 이면 
        if naver_shop == -1:

            naver_shop = input_url.find('search.shopping.naver.com')

            if naver_shop == -1:
                c_type = -1

            else :
                c_type = 2

        else :
            c_type = 1
        #===============================================================================
        if c_type == 1:
            
            self.smart()
           
        elif c_type == 2:
            
            self.search()
            
        else:
            self.driver.close()

            # 팝업 창 닫기 
            if len(self.driver.window_handles) >1:
                last_tab = self.driver.window_handles[1]
                self.driver.switch_to.window(window_name=last_tab)
                self.driver.close()
            last_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(window_name=last_tab)
#====================================================================================================== 
    def fcrawgo(self): # 5번
        for keywords in self.matching_word_one:
            for keyword in keywords: # 중복제거, 결측치 제거하여 총 98개의 키워드가 존재함
                type_this = str(keyword) # 문자형으로 다 바꿔
                if type_this != 'nan': # 키워드가 존재하면 들어가
                    print(f'값 is not None!! >> {keyword}')

                    # 키워드별로 본사의 아이템 긁는게 다르니까 A키워드가 n개들어있다를 알려는거
                    company_count = self.find_keyword.count(keyword) 

                    self.index_number = 0 # 키워드 바뀔때 마다 상품 인덱스번호 초기화

                    # 검색 창 찾기 - 네이버 기준
                    try:
                        elem = self.driver.find_element_by_name("query")
                    except:
                        elem = self.driver.find_element_by_class_name("searchInput_search_input__1Eclz")

                    elem.clear()
                    # 제품명 변수 지정
                    self.pd_name = keyword

                    # 찾은 검색 창에 검색 
                    elem.send_keys(self.pd_name)
                    time.sleep(1)

                    # 엔터 
                    elem.send_keys(Keys.RETURN)
                    time.sleep(2)
                    try:
                        no_search = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.noResult_no_result__1ad0P > p').text
                        elem.send_keys(Keys.RETURN)
                        time.sleep(3)
                    except:
                        pass
                #======================================================================================================
                    for i in range(5):
                        self.driver.execute_script("window.scrollTo(0, 9000)")
                        time.sleep(1)

                    html = self.driver.page_source # 헌재 페이지 소스 가져오기
                    soup = BeautifulSoup(html, "html.parser") # 담은 웹페이지를 뷰티풀 수프로 불러오기
                    total_items = soup.select('li.basicList_item__2XT81')

                    #  전체 상품수
                    items = int(self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.seller_filter_area > ul > li.active > a > span.subFilter_num__2x0jq').text.replace(',',''))
                    print(f'items >> {items}')

                    while True:
                        self.while_count += 1 # while문 제어용

                        # 현페이지 상품 갯수 - 다음버튼 누를때 마다 달라짐
                        now_page_items = len(self.driver.find_elements_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div'))
                        print(f'now_page_items >> {now_page_items}')

                        for item in total_items: # 저 안에 한장 들엇어 hmtl 그 안에서 해당되는거 하나씩 가져오는건데 저거 1초컷이야

                            self.this_tem_number += 1

                            try:
                                iis_ad = item.select_one('button.ad_ad_stk__12U34').text
                            except:
                                iis_ad = None

                            print(f'self.rank_num >> {self.rank_num}')

                            if iis_ad != '광고':
                                self.rank_num += 1 # 여기 있으면 광고는 전부 스킵하고 숫자 올라감

                                try:
                                    self.seller_name = item.select_one('a.basicList_mall__sbVax').text
                                except:
                                    self.seller_name = None

                                self.title = item.select_one('a.basicList_link__1MaTN').get('title')
                                
                                if self.title in self.find_title: # self.find_title 여기엔 공백이랑 중복이랑 다 제거된채 만들어진 리스트 
                                    self.all_count += 1 #이거 company_count 랑 같으면 끝
                                    print('제품명 >> {}'.format(self.title))

                                    # self.find_titles 이거 리스트로 만든건데 935개 안에서 해당되는 타이틀이 어디몇번째냐 보는거
#                                     how_title_num = self.find_titles.index(title)
                                    res_list = [i for i, value in enumerate(self.find_titles) if value == self.title] 
                                    for index in res_list: # 해당되는 value값의 인덱스 위치가 나올거야
                                        self.cook_it_this.loc[index,['rank']] = self.rank_num
                                        
                                        insertlist = list(self.cook_it_this.iloc[[index][0]])
                        
                                        NvProduct(
                                        rank_num = insertlist[0],
                                        item_code = insertlist[1],
                                        keyword = insertlist[2],
                                        title = insertlist[3],
                                        price = insertlist[4].replace(',',''),
                                        review_count = insertlist[5],
                                        serial_number = insertlist[6],
                                        prod = insertlist[7],
                                        link = insertlist[8],
                                        score_avg = insertlist[9],
                                        image = insertlist[10],
                                        item_states = insertlist[11]
                                        ).save()
                                        time.sleep(1)

                                    # 상품 리뷰는 안긁었어 처음에 그래서 이거 들어가야되
                                    # 들어가면 리뷰만 긁도록 만들어놨어
                                    # 타사면 상정과 상리 둘다
                                    #보사면 상리만
                                    self.in_crawling()
#                                     self.come_url += 1

                                else:
                                    if self.othercheck <= 3:
                                        # 타사네? 먼저 self.come_url 위치의 '매칭키워드'컬럼에 self.pd_name값을 넣고 들어가
                                        self.cook_it_this.loc[self.come_url,['매칭키워드']] = self.pd_name
                                        self.in_crawling()
                                        self.othercheck += 1
                                        
                                        #  self.in_crawling() 들어가서 스마트든 써치든 긁어담았지? 그리고 다음거 준비하러 나올때 
                                        # 여기서 1 먹고 준비하러 가는거지
                                        self.come_url += 1 # 타사도 인덱스 번호를 부여 해야 하니까
                                    else:
                                        pass
                                

                                print('★ ★ ★ ★ ★ ★ 다음 드루와 ★ ★ ★ ★ ★ ★')
                        time.sleep(1)
                        pageing = round(items / now_page_items )

                        if self.all_count == company_count : #  self.all_count 본사제품 하나씩 먹다가 company_count 되면 들어감 company_count는 키워드마다 다름
                            self.rank_num = 0 # 랭킹 카운트 키워드 버뀌면 이건 리셋
                            self.while_count = 0 # while_count 초기화 키워드 바꼈으니 리셋
                            self.this_tem_number = 0 # 상품태그 초기화(1~ 46 까지) 키워드 바낄거니까 리셋
                            self.othercheck = 1 # 바뀐 키워드의 타사상품 또 3개 가져와야지
                            # 여기는 제품 1번부터 N번까지 전체 다 긁으면 넣어가는 부분인데 아래 숫자를 100을로 지정해 놔서 쓸데는 없어 하지만 나중에 필요할지 몰라 놔뒀지
                            break

                        elif self.rank_num >= 100:
                            # 리스트 불러와서 value값에 원하는거 넣고 그거 몇번째인지.. 근데 나도 잘 모르겠다이거 원리가
                            res_list = [i for i, value in enumerate(self.matching_keyword_lists) if value == keyword]
                            for index in res_list:
                                self.cook_it_this.loc[index,['rank']] = '100위권밖'

                                insertlist = list(self.cook_it_this.iloc[[index][0]])
#이거 살려
                                NvProduct(
                                rank_num = insertlist[0],
                                item_code = insertlist[1],
                                keyword = insertlist[2],
                                title = insertlist[3],
                                price = insertlist[4],
                                review_count = insertlist[5],
                                serial_number = insertlist[6],
                                prod = insertlist[7],
                                link = insertlist[8],
                                score_avg = insertlist[9],
                                image = insertlist[10],
                                item_states = insertlist[11]
                                ).save()
                            self.rank_num = 0 # 랭킹 카운트 키워드 버뀌면 이건 리셋
                            self.while_count = 0 # while_count 초기화 키워드 바꼈으니 리셋
                            self.this_tem_number = 0 # 상품태그 초기화(1~ 46 까지) 키워드 바낄거니까 리셋
                            self.othercheck = 1 # 바뀐 키워드의 타사상품 또 3개 가져와야지
                            break

                        try:
                            next_item_button = self.driver.find_element_by_css_selector('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.pagination_pagination__6AcG4 > a.pagination_next__1ITTf')
                            next_item_button.send_keys(Keys.RETURN)
                            self.this_tem_number = 0 # 상품태그 초기화(1~ 46 까지)
                            time.sleep(1.5)

                        except:
                            self.rank_num = 0 # 랭킹 카운트 키워드 버뀌면 이건 리셋
                            self.while_count = 0 # while_count 초기화 키워드 바꼈으니 리셋
                            self.this_tem_number = 0 # 상품태그 초기화(1~ 46 까지) 키워드 바낄거니까 리셋
                            self.othercheck = 1 # 바뀐 키워드의 타사상품 또 3개 가져와야지
                            break 

                else: # 키워드가 None인거 여기는 한번밖에 안들어가진다 None이 한개뿐이라서
                    print(f'값 is Non? >> {keyword}')
                    res_list = [i for i, value in enumerate(self.matching_keyword_lists) if value != "쓰레기통" and value != "분리수거함" and value != "음식물쓰레기통" and value != "행거" and value !="멀티탭정리함" and value != "비닐정리함" and value != "리빙박스" and value != "트롤리" and value != "기저귀정리함" and value != "펜트리정리함" and value != "싱크롤매트" and value != "조리도구" and value != "욕실매트" and value != "조리도구걸이" and value != "세탁망" and value != "아기거품목욕" and value != "도어쿠션" and value != "자석도어스토퍼" and value != "문닫힘방지" and value != "모서리보호대" and value !="초음파키재기" and value != "아기손톱깎이" and value != "유아전동칫솔" and value != "네일트리머" and value != "전선몰딩" and value != "변기커버" and value != "찍찍이테이프" and value !="벽걸이" and value != "미끄럼방지테이프" and value != "폼블럭" and value != "스위치커버" and value != "애견매트" and value != "전선정리" and value != "창문잠금장치" and value != "욕실미끄럼방지매트" and value != "걸레받이" and value != "벽매트" and value != "타일시트지" and value != "애견욕조" and value != "고양이화장실" and value != "스크레쳐" and value != "급수기" and value != "사료보관통" and value !="방충망" and value != "세탁기받침" and value != "애견식기" and value !="롤매트" and value !="유아변기커버" and value != "의자발커버" and value !="소음방지패드" and value !="스크래쳐" and value !="물구멍방충망" and value !="문풍지" and value !="공구함" and value !="문손잡이커버" and value !="흡착이유식판"and value !="실리콘 턱받이"and value != "남아소변기"and value != "아기변기" and value != "의자발커버테니스공" and value != "물흡수테이프" and value !="차량용컵홀더" and value !="문쾅방지" and value !="샷시손잡이" and value !="아기수영장" and value != "아기의자" and value != "퍼즐매트"and value != "부스터" and value != "하이체어" and value != "아기마스크" and value != "모기퇴치팔찌" and value != "아기바리깡" and value != "서랍잠금장치" and value != "냉장고잠금장치" and value != "콘센트안전커버" and value != "문고리잠금" and value !="콘센트가리개" and value != "가스렌지안전가드" and value !="아기샴푸캡" and value !="유모차걸이" and value != "미아방지끈" and value != "기저귀봉투" and value !="디딤대" and value != "아기무릎보호대" and value != "안전문" and value !="유모차가방" and value !="킥매트" and value !="헤드레스트" and value !="차량용목쿠션" and value != "수도꼭지연장" and value != "아기욕조" and value != "카시트후방거울" and value !="카시트트레이" and value !="햇빛가리개" and value != "아기걸음마보조기" and value != "유모차공기청정기" and value != "머리쿵보호대" and value != "롤매트테이프" and value != "유모차핸드폰거치대" and value != "아기머리보호대"]
                    for index in res_list:
                        print('실행됨1')
                        self.cook_it_this.loc[index,['rank']] = '측정불가'

                        insertlist = list(self.cook_it_this.iloc[[index][0]])

                        NvProduct(
                        rank_num = insertlist[0],
                        item_code = insertlist[1],
                        keyword = insertlist[2],
                        title = insertlist[3],
                        price = insertlist[4],
                        review_count = insertlist[5],
                        serial_number = insertlist[6],
                        prod = insertlist[7],
                        link = insertlist[8],
                        score_avg = insertlist[9],
                        image = insertlist[10],
                        item_states = insertlist[11]
                        ).save()
                    # = = = = = = = = = = = 키워드가 None이면 들어가 그리고 여긴 한번밖에 안들어올꺼야
                    try:
                        print('실행됨2')
                        # 935개에 해당하는것만이어야됨
                        res_list = [i for i, value in enumerate(self.this_url_list) if value == 'url없음']
                        for index in res_list:
                            print('실행됨2_들어왔으')
                            self.cook_it_this.loc[index,['rank']] = '측정불가'

                            insertlist = list(self.cook_it_this.iloc[[index][0]])

                            NvProduct(
                            rank_num = insertlist[0],
                            item_code = insertlist[1],
                            keyword = insertlist[2],
                            title = insertlist[3],
                            price = insertlist[4],
                            review_count = insertlist[5],
                            serial_number = insertlist[6],
                            prod = insertlist[7],
                            link = insertlist[8],
                            score_avg = insertlist[9],
                            image = insertlist[10],
                            item_states = insertlist[11]
                            ).save()

                    except:
                        pass
                    # = = = = = = = = = = = url이 없는 경우는 전부 랭크 None
                    try:
                        print('실행됨3')
                        res_list = [i for i, value in enumerate(self.this_item_state_list) if value == '이 상품은 현재 판매중지 된 상품입니다.' or value == '상품이 존재하지 않습니다.']
                        for index in res_list:
                            print('실행됨3_들어왔으')
                            self.cook_it_this.loc[index,['rank']] = '측정불가'

                            insertlist = list(self.cook_it_this.iloc[[index][0]])

                            NvProduct(
                            rank_num = insertlist[0],
                            item_code = insertlist[1],
                            keyword = insertlist[2],
                            title = insertlist[3],
                            price = insertlist[4],
                            review_count = insertlist[5],
                            serial_number = insertlist[6],
                            prod = insertlist[7],
                            link = insertlist[8],
                            score_avg = insertlist[9],
                            image = insertlist[10],
                            item_states = insertlist[11]
                            ).save()
                    except:
                        pass
        self.driver.close()