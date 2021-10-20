from django.contrib import messages, auth
from django.shortcuts import redirect, render
from .forms import  SignupForm



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "로그인완료")
            # return render(request,'main/main.html')
            return redirect('main')
        else:
            messages.success(request, "회원정보없음")
            return render(request,'accounts/login_form.html')
    else:
        return render(request, 'accounts/login_form.html')



def logout(request):
    auth.logout(request)
    return redirect('accounts/login_form.html')




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "회원가입 환영합니다.")
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html',{
        'form':form,
    } )