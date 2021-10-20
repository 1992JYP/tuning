from django.http import request
from django.shortcuts import render

# Create your views here.
def trand_Transitionapp_list (reqeust):
    return render(request, "trand_Transitionapp/list.html",context={})