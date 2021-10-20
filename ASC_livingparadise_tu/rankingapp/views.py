from django.shortcuts import render

# Create your views here.
def ranking_list(request):
    return render(request , 'rankingapp/list.html', context={})