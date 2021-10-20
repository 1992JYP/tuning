from django.shortcuts import render

# Create your views here.
def review_list(request):
    return render(request , 'reviewapp/list.html', context={})