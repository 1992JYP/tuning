from crawling.models import Cp_c_Product
from typing import List
from django.core import paginator
from django.db.models.expressions import Value
from django.urls.base import reverse_lazy
from apps.main.Crawlers.naverCrawler import naverCrawler
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.paradise import models as lpmodels
from apps.main import models
from django.urls import reverse
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
import time
import pandas as pd
# from tqdm import tqdm_notebook
# from selenium.webdriver.common.alert import Alert4
from apps.main.Crawlers.naverCrawler import naverCrawler

from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from crawling.models import ProductState

import json

@login_required
def home(request):
    Query = lpmodels.CpProduct.objects.filter(keyword='안전문')
    template = loader.get_template('main/home.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'test' : Query
    }
    return HttpResponse(template.render(context, request))





@login_required
def main(request):
    # 입력된 검색어 가져오기
    DASHBOARD_Search = request.POST.get('DASHBOARD_Search')

    # 선택한 버튼 가져오기
    DASHBOARD_Search_btn = request.POST.get('radio')
    print("버튼 데이터 값 : ",DASHBOARD_Search_btn)


    if request.method == "POST":
        

        # 검색만 했을 때 
        if DASHBOARD_Search != None:
            ## 데이터 필터링
            DASHBOARD_table_total = lpmodels.ProductMaster.objects.filter(
            Q(pd_name__contains=DASHBOARD_Search) | Q(pd_code__contains=DASHBOARD_Search) |
            Q(pd_brand__contains=DASHBOARD_Search) | Q(pd_keyword__contains=DASHBOARD_Search) |
            Q(nv_code__contains=DASHBOARD_Search) | Q(pd_manager__contains=DASHBOARD_Search)).values()

            # 검색어 추출 후 페이징 처리
            paginator_Search = Paginator(DASHBOARD_table_total, 10)
            page = request.GET.get('page','1')
            page_obj_Search = paginator_Search.get_page(page)
           
            print("출력값 확인 됨1",DASHBOARD_Search)
            context = {    
                'Query' : page_obj_Search,     
            }

                
                

        # 버튼 누르고 정렬    
        if DASHBOARD_Search_btn !=None:
            print("출력값 확인 됨",DASHBOARD_Search_btn)
            DASHBOARD_Search_btn_order = list(lpmodels.ProductMaster.objects.order_by(DASHBOARD_Search_btn).values())
            
            # 검색어 추출 후 페이징 처리
            paginator_Search = Paginator(DASHBOARD_Search_btn_order, 10)
            page = request.GET.get('page','1')
            page_obj_Search = paginator_Search.get_page(page)


            context = {    
                'Query' : page_obj_Search ,     
            }

        
        


    elif request.method == "GET":
        DASHBOARD_table_total = lpmodels.ProductMaster.objects.all()

        paginator_Search = Paginator(DASHBOARD_table_total, 10)
        page = request.GET.get('page','1')
        page_obj_Search = paginator_Search.get_page(page)


        context = {    
                'Query' :  page_obj_Search ,     
            }



     
 
    return HttpResponse(loader.get_template('main/main.html').render(context, request))











@login_required
def keyword(request):
    key = request.GET.get('key')
    print("출력확인 : ",key)


    if request.method == "GET":


        if key == None:
            rank_today = ProductState.objects.all().order_by('id')


            paginator =Paginator(rank_today,13)
            page_number =request.GET.get('page')
            page_obj= paginator.get_page(page_number)


            context = {
                'ranking' : page_obj,

            }
            return HttpResponse(loader.get_template('main/keyword.html').render(context, request))

        else:
            rank_today = ProductState.objects.all().filter(pd_name__icontains=key)

            rank_today_nv = ProductState.objects.all().filter(pd_name__icontains=key,pd_state__icontains='naver').order_by()[:3]
            rank_today_cp = ProductState.objects.all().filter(pd_name__icontains=key).filter(~Q(pd_state__icontains='naver')).order_by()[:3]


            paginator =Paginator(rank_today,13)
            page_number =request.GET.get('page')
            page_obj= paginator.get_page(page_number)



            context = {
                'ranking' : page_obj,
                'rank_today_nv' : rank_today_nv,
                'rank_today_cp' : rank_today_cp

            }
            return HttpResponse(loader.get_template('main/keyword.html').render(context, request))

    






@login_required
def review(request):
    template = loader.get_template('main/review.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))







@login_required
def Dashboard(request):
    print('대시보드')
    ## 랭킹 
    # 오늘꺼 
    
    Query_to = Cp_c_Product.objects.filter(company='0').filter(date_info__icontains='09-24').values()[:20]
    today_list =[] 
    for q in Query_to.values_list():
        today_list.append(q)

    result_list = []
    for to in today_list:
        try:
            Query_y = Cp_c_Product.objects.get(title=to[6],keyword=to[5],date_info__icontains='09-23')
            f = Query_y.pd_index
            cf =  f - to[1]  
        except:
            f = 0
        t = list(to)
        t.append(f)
        t.append(cf)
        result_list.append(t)
    Query_top = result_list[:3]



    context = {

        'rankingchange' : result_list,
        'rankingchange_top' : Query_top,
        
     
    }

    template = loader.get_template('main/Dashboard.html')
    return HttpResponse(template.render(context, request))









@login_required
def dbtest(request):



    # dbtesttext.delete()
    namequery = request.POST.get('name','')
    posquery = request.POST.get('position','')
    phonequery = request.POST.get('phone','')
    # namequery = request.POST['btntest123']a
    # cs = naverCrawler()
    # print(cs.fcrawgo())
    if request.POST.get('btncheck','')=='1':
        dbtesttext = models.Employees.objects.filter(name=namequery)
  
    elif request.POST.get('btncheck','')=='2':
        dbtesttext = models.Employees.objects.create(name=namequery,position=posquery,phone=phonequery)
        dbtesttext = models.Employees.objects.all()
    else:    
        dbtesttext = models.Employees.objects.all()

    template = loader.get_template('main/dbtest.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'test' : dbtesttext,
        'name' : '''namequery'''
        # 'modeltest' : modeltest
        # 'testtext' : request
    }
    return HttpResponse(template.render(context, request))



@login_required
def login(request):
    template = loader.get_template('main/login.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))




@login_required
def review_Dashboard(request):
    keyword = request.GET.get('code')
    main =lpmodels.ProductMaster.objects.filter(pd_code=keyword)[0]
    total =lpmodels.Totalresult.objects.filter(prod_id=keyword)[0]
    key =lpmodels.Totalkeyword.objects.filter(prod_id=keyword).order_by('-key_grade')
    if len(key)>10:
        key = key[0:10]
    keys =lpmodels.Totalsentence.objects.filter(prod_id=keyword)    
    if len(keys)>10:
        keys = keys[0:10]
    emo =lpmodels.Emokeyword.objects.filter(prod_id=keyword).order_by('-key_grade')
    if len(emo)>10:
        emo = emo[0:10]
    emos =lpmodels.Emosentence.objects.filter(prod_id=keyword)
    if len(emos)>10:
        emos = emos[0:10]
    # template = loader.get_template('main/review_Dashboard.html')
    context = {
        'total' : total,
        'main' : main,
        'key' : key,
        'keys' : keys,
        'emo' : emo,
        'emos' : emos
    }
    return HttpResponse(template.render(context, request))

# def home(request):
#     template = loader.get_template('main/home.html')
#     context = {
#         'key_number': '1',
#         'key_rank' : '순위1',
#         'review_number': '1',
#         'review_rank' : '순위1',
#     }
#     return HttpResponse(template.render(context, request))


    
    
    



# def home_key(request):
#     keyword = '안전문'
#     Query = lpmodels.CpProduct.objects.filter(keyword='안전문').filter(date_info__gte='2021-07-05').exclude(change_index=0).exclude(change_index=9999)[:7]
#     template = loader.get_template('main/home_key.html')
#     context = {
#         'some_dynamic_value': 'This text comes from django view!',
#         'test' : Query
#     }
#     return HttpResponse(template.render(context, request))

# def home_review(request):
#     template = loader.get_template('main/home_review.html')
#     context = {
#         'some_dynamic_value': 'This text comes from django view!',
#     }
#     return HttpResponse(template.render(context, request))


# def home_review_search(request):
    template = loader.get_template('main/home_review_search.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
    }
    return HttpResponse(template.render(context, request))

def dbtest(request):
    # dbtesttext.delete()
    namequery = request.POST.get('name','')
    posquery = request.POST.get('position','')
    phonequery = request.POST.get('phone','')
    # namequery = request.POST['btntest123']
    # cs = naverCrawler()
    # print(cs.fcrawgo())
    if request.POST.get('btncheck','')=='1':
        dbtesttext = models.Employees.objects.filter(name=namequery)
  
    elif request.POST.get('btncheck','')=='2':
        dbtesttext = models.Employees.objects.create(name=namequery,position=posquery,phone=phonequery)
        dbtesttext = models.Employees.objects.all()
    else:    
        dbtesttext = models.Employees.objects.all()

    template = loader.get_template('main/dbtest.html')
    context = {
        'some_dynamic_value': 'This text comes from django view!',
        'test' : dbtesttext,
        'name' : '''namequery'''
        # 'modeltest' : modeltest
        # 'testtext' : request
    }
    return HttpResponse(template.render(context, request))



class ModelCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('')
    template_name = "main/create.html"

