from django.shortcuts import render

# Create your views here.

def HomePage(request):
    pass

def SignupPage(request):
    return render (request,'register.html')

def LoginPage(request):
    return render (request,'login.html')