from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from login_register_app.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Income, Profile, Expense

# Graphs
from datetime import datetime
import numpy as np
import pandas as pd
import base64

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
    user = request.user
    incomes = Income.objects.filter(user=user).order_by('-created_at')
    expenses = Expense.objects.filter(user=user).order_by('-created_at')

    history = []
    for income in incomes:
        history.append((income.created_at, f"Income of {income.amount}€ from {income.source}"))

    for expense in expenses:
        history.append((expense.created_at, f"Expense of {expense.amount}€ for {expense.source}"))

    history = sorted(history, key=lambda x: x[0], reverse=True)

    context = {'history': history}
    return render(request, 'history.html', context)

@login_required(login_url='login')
def GraphsPage(request):
    data = Income.objects.filter(user=request.user).values('source', 'amount', 'created_at')
    df = pd.DataFrame(list(data))
    df['created_at'] = pd.to_datetime(df['created_at']).dt.to_period('M')
    df['amount'] = df['amount'].astype('float')
    df = df.groupby(['created_at', 'source']).sum().replace('', np.nan).reset_index()
    df['source'] = df['source'].fillna('')
    # Create a new dataframe with a row for each month in the year
    today = datetime.today()
    months = pd.date_range(start=f'{today.year}-01-01', end=f'{today.year}-12-01', freq='MS').to_period('M')
    sources = df['source'].dropna().unique()  # usunięcie wartości NaN
    empty_df = pd.DataFrame({'created_at': months})
    for source in sources:
        empty_df[source] = np.nan
    df = pd.concat([df, empty_df], ignore_index=True)
    df = df.sort_values('created_at')

    # Pivot the dataframe and fill missing values with 0
    df = df.replace(np.nan, '', regex=True)
    df = df.pivot(index='created_at', columns='source', values='amount').fillna(0)

    # Plot the chart
    chart = df.plot(kind='bar', stacked=True, figsize=(12, 8))
    chart.set_xlabel('Month')
    chart.set_ylabel('Amount')
    chart.set_title('Cash inflow per source per month')
    chart.legend(title='Source', loc='upper left')

    chart.figure.tight_layout()
    chart.figure.savefig('chart.png')  # Save chart to file
    with open('chart.png', 'rb') as f:
        chart_data = f.read()
        chart_data_base64 = base64.b64encode(chart_data).decode('utf-8')
    return render(request, 'graphs.html', {'chart_data': chart_data_base64})


@login_required(login_url='login')
def GoalsPage(request):
    return render (request,'goals.html')

@login_required(login_url='login')
def TipsPage(request):
    return render (request,'tips.html')
