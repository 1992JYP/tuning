from django.shortcuts import render
from dashboardapp.models import ProductMaster as pd

# Create your views here.
def dashboard_list(request):

    DASHBOARD_table_total = pd.objects.all()

    context={
        'Query' : DASHBOARD_table_total
    }

    return render(request , 'dashboardapp/list.html', context )

def review_dashboard_list(request):
    
   

    context={
       
    }

    return render(request , 'dashboardapp/review_dashboard.html', context )



##네이버
def Sold_out_nv(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/naver_popup/Sold_out_nv.html', context )
def grade_nv(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/naver_popup/grade_nv.html', context )
def ranking_top_five_nv(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/naver_popup/ranking_top_five_nv.html', context )
def lowest_price_nv(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/naver_popup/lowest_price_nv.html', context )
def ranking_up_nv(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/naver_popup/ranking_up_nv.html', context )
def review_lowest_nv(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/naver_popup/review_lowest_nv.html', context )


## 쿠팡
def Sold_out_cp(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/coupang_popup/Sold_out_cp.html', context )
def grade_cp(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/coupang_popup/grade_cp.html', context )
def ranking_top_five_cp(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/coupang_popup/ranking_top_five_cp.html', context )
def lowest_price_cp(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/coupang_popup/lowest_price_cp.html', context )
def ranking_up_cp(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/coupang_popup/ranking_up_cp.html', context )
def review_lowest_cp(request):

   

    context={
        
    }

    return render(request , 'dashboardapp/coupang_popup/review_lowest_cp.html', context )







