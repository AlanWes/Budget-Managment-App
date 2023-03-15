from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        c_password=request.POST.get('confirm_password')
        my_user=User.objects.create_user(uname, email, password)
        my_user.save()
        return HttpResponse("User created account!")
        print(uname, email, password, c_password)

    return render (request,'register.html')

def LoginPage(request):
    return render (request,'login.html')