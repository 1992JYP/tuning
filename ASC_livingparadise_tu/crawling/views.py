## 작성 2021-06-17  - 이유인 
## 수정  2021- 07-05  - 이유인

from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
from datetime import datetime , timedelta
import time
import re
import os
from openpyxl import load_workbook
from .models import Cp_c_Product , Cp_review
from django.db import connection
from tqdm import tqdm
from crawling.coupang_crawler import coupangCrawler

# def item_select(request):
#     Cp_c_Product.object.filter()



# linux cron 사용 - 예약 작업 스케쥴러  



# 아이템 검색
def item_search(request):
    today = datetime.now()
    today = today.strftime("%Y-%m-%d")
    
    qs = Cp_c_Product.objects.all()
    qs = qs.filter(date_info__icontains=today,
                    pd_index__lt = 101  )
    qs = qs.filter(change_index__lt = 100,
                     ).order_by('-change_index')[0:7]
    for item in qs:
        print(item.title)
        print(item.change_index)
    return render(request,'main/home_key.html',{
        'item_list':qs,
        })




def item_crawling(request):
    cl = coupangCrawler()
    cl.search_listup()
    cl.item_search()
    cl.item_review()
    return render(request,'okok',{
        'tiem':'ts',
        })



def item_detail(request):
    pid = request.GET.get('pid','')
    iid = request.GET.get('iid','')
    qs = Cp_c_Product.objects.all()
    qs= qs.filter(product_id__icontains=pid,item_id__icontains=iid).first()
    return render(request, 'main/home_keyword_main.html',{
       'item_detail': qs,
   })        

def allItemCount(request):
    q = request.GET.get('q', '')
    cl = coupangCrawler()
    print(q)
    itemCount = cl.itemSearchCount(q)
    return render(request, 'crawling/item_list.html',{
        'allItemCount': itemCount,
    })