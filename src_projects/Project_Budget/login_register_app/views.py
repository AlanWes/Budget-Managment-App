from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from login_register_app.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Income, Profile, Expense

def MasterPage(request):
    return render (request,'master.html')

def RegisterPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        c_password=request.POST.get('confirm_password')
        money=request.POST.get('money')
        # Validation
        if password==c_password:
            if len(password) < 8:
                return render(request, 'register.html', {'error_message': 'Password must contain at least 8 characters.'})
            elif not any(char.isdigit() for char in password):
                return render(request, 'register.html', {'error_message': 'Password must contain at least one number.'})
            elif not any(char.isupper() for char in password):
                return render(request, 'register.html', {'error_message': 'Password must contain at least one uppercase character.'})
            else:
                try:
                    money = float(money)
                except ValueError:
                    return render(request, 'register.html', {'error_message': 'Invalid money value.'})
                user = User.objects.create_user(username=uname, email=email, password=password)
                profile = Profile.objects.create(user=user, money=money)
                messages.success(request, 'Your account has been created successfully!')
                return redirect('login')
        else:
            return render(request, 'register.html', {'error_message': "Those passwords didn't match. Try again."})

    return render (request,'register.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('login_pass')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Username or Password is incorrect.'})
       
    return render (request,'login.html')

@login_required(login_url='login')
def HomePage(request):
    user_profile = Profile.objects.get(user=request.user)
    money = user_profile.money
    expense = user_profile.spend

    if request.method == 'POST':
        income_source = request.POST.get('source-income')
        expense_source = request.POST.get('source-expense')
        new_income = request.POST.get('new_income')
        new_expense = request.POST.get('new_expense')

        if new_income is not None and new_income != '':
            new_income = int(new_income)
            user_profile.money += new_income
            Income.objects.create(user=user_profile.user, amount=new_income, source=income_source)
            user_profile.save()

        if new_expense is not None and new_expense != '':
            new_expense = int(new_expense)
            user_profile.spend += new_expense
            user_profile.money -= new_expense
            Expense.objects.create(user=user_profile.user, amount=new_expense, source=expense_source)
            user_profile.save()

        money = user_profile.money
        expense = user_profile.spend

    return render(request, 'home.html', {'money': money, 'expense': expense})

def LogoutPage(request):
    logout(request)
    return redirect('master')

@login_required(login_url='login')
def HistoryPage(request):
    return render (request,'history.html')

@login_required(login_url='login')
def GraphsPage(request):
    return render (request,'graphs.html')

@login_required(login_url='login')
def GoalsPage(request):
    return render (request,'goals.html')

@login_required(login_url='login')
def TipsPage(request):
    return render (request,'tips.html')
