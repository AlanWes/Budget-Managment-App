from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum
from login_register_app.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Income, Profile, Expense, Goal
from decimal import Decimal

# Graphs
from datetime import datetime
import numpy as np
import pandas as pd
import base64
import os

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
            new_income = Decimal(new_income)
            user_profile.money += new_income
            Income.objects.create(user=user_profile.user, amount=new_income, source=income_source)
            user_profile.save()

        if new_expense is not None and new_expense != '':
            new_expense = Decimal(new_expense)
            user_profile.spend += new_expense
            user_profile.money -= new_expense
            Expense.objects.create(user=user_profile.user, amount=new_expense, source=expense_source)
            user_profile.save()

        money = user_profile.money
        expense = user_profile.spend

    return render(request, 'home.html', {'money': "{:.2f}".format(money).rstrip('0').rstrip('.'), 'expense': "{:.2f}".format(expense).rstrip('0').rstrip('.')})

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

colors_income = {'business': '#e377c2', 
          'e_commerce': '#1f77b4', 
          'employment': '#d62728', 
          'intellectual': '#ff7f0e', 
          'investment': '#2ca02c', 
          'other': '#7f7f7f', 
          'rental': '#9467bd', 
          'social_security': '#bcbd22',
        }

colors_expense = {
          'house': '#8c564b',
          'food': '#ff9896',
          'clothes': '#9edae5',
          'transport': '#98df8a',
          'entertaiment': '#aec7e8',
          'utility': '#ffbb78',
          'loan': '#f7b6d2',
          'healthcare': '#c5b0d5',
          'invest': '#c49c94'
        }


@login_required(login_url='login')
def GraphsPage(request):
    income_data = Income.objects.filter(user=request.user).values('source', 'amount', 'created_at')
    expense_data = Expense.objects.filter(user=request.user).values('source', 'amount', 'created_at')

    if income_data.exists():
        income_df = pd.DataFrame(list(income_data))
        income_df['created_at'] = pd.to_datetime(income_df['created_at']).dt.to_period('M')
        income_df['amount'] = income_df['amount'].astype('float')
        income_df = income_df.groupby(['created_at', 'source']).sum().replace('', np.nan).reset_index()
        income_df['source'] = income_df['source'].fillna('')

        today = datetime.today()
        months = pd.date_range(start=f'{today.year}-01-01', end=f'{today.year}-12-01', freq='MS').to_period('M')

        income_sources = ['business', 'e_commerce', 'employment', 'intellectual', 'investment', 'other', 'rental', 'social_security']
        empty_income_df = pd.DataFrame({'created_at': months})
        for source in income_sources:
            empty_income_df[source] = np.nan
        income_df = pd.concat([income_df, empty_income_df], ignore_index=True)
        income_df = income_df.sort_values('created_at')
        income_df = income_df.replace(np.nan, '', regex=True)
        income_df = income_df.pivot(index='created_at', columns='source', values='amount').fillna(0)
        income_df = income_df.reindex(columns=[x for x in colors_income.keys()])

        chart1 = income_df[income_df.columns.intersection(income_sources)].plot(kind='bar', stacked=True, figsize=(12, 8), color=[colors_income.get(x, 'red') for x in income_df.columns])
        chart1.set_xlabel('Month')
        chart1.set_ylabel('Amount')
        chart1.set_title('Cash inflow per source per month')
        chart1.legend(title='Source', loc='upper left')
        chart1.figure.set_facecolor('#FFFAFA')

        chart1.figure.tight_layout()
        chart1.figure.savefig('chart1.png')

        with open('chart1.png', 'rb') as f:
            chart_data_1 = f.read()
            chart_data_1_base64 = base64.b64encode(chart_data_1).decode('utf-8')

    else:
        chart_data_1_base64 = None

    if expense_data.exists():
        expense_df = pd.DataFrame(list(expense_data))
        expense_df['created_at'] = pd.to_datetime(expense_df['created_at']).dt.to_period('M')
        expense_df['amount'] = expense_df['amount'].astype('float')
        expense_df = expense_df.groupby(['created_at', 'source']).sum().replace('', np.nan).reset_index()
        expense_df['source'] = expense_df['source'].fillna('')

        today = datetime.today()
        months = pd.date_range(start=f'{today.year}-01-01', end=f'{today.year}-12-01', freq='MS').to_period('M')

        expense_sources = ['house', 'food', 'clothes', 'transport', 'entertaiment', 'utility', 'loan', 'healthcare', 'invest', 'other']
        empty_expense_df = pd.DataFrame({'created_at': months})
        for source in expense_sources:
            empty_expense_df[source] = np.nan
        expense_df = pd.concat([expense_df, empty_expense_df], ignore_index=True)
        expense_df = expense_df.sort_values('created_at')
        expense_df = expense_df.replace(np.nan, '', regex=True)
        expense_df = expense_df.pivot(index='created_at', columns='source', values='amount').fillna(0)
        expense_df = expense_df.reindex(columns=[x for x in colors_expense.keys()])

        chart2 = expense_df[expense_df.columns.intersection(expense_sources)].plot(kind='bar', stacked=True, figsize=(12, 8), color=[colors_expense.get(x, 'red') for x in expense_df.columns])
        chart2.set_xlabel('Month')
        chart2.set_ylabel('Amount')
        chart2.set_title('Cash outflow per source per month')
        chart2.legend(title='Source', loc='upper left')
        chart2.figure.set_facecolor('#FFFAFA')

        chart2.figure.tight_layout()
        chart2.figure.savefig('chart2.png')

        with open('chart2.png', 'rb') as f:
            chart_data_2 = f.read()
            chart_data_2_base64 = base64.b64encode(chart_data_2).decode('utf-8')

    else:
        chart_data_2_base64 = None

    return render(request, 'graphs.html', {'chart_data_1': chart_data_1_base64, 'chart_data_2': chart_data_2_base64})

@login_required(login_url='login')
def GoalsPage(request):
    goals = Goal.objects.filter(user=request.user)
    if request.method == 'POST':
        goal_name = request.POST['goal_name']
        goal_number = request.POST['goal_number']
        source_income = request.POST['source_income']
        button_value = request.POST.get('button')

        if button_value == 'create':
            goal = Goal.objects.create(
                goal_name=goal_name,
                goal_number=goal_number,
                source_income=source_income,
                user=request.user
            )
            return redirect('goals')
        elif button_value == 'finished':
            goal_id = request.POST['goal_id']
            goal = Goal.objects.get(id=goal_id)
            goal.is_finished = True
            goal.save()
            return redirect('goals')
        elif button_value == 'delete':
            goal_id = request.POST['goal_id']
            goal = Goal.objects.get(id=goal_id)
            goal.delete()
            return redirect('goals')

    return render(request, 'goals.html', {'goals': goals})


@login_required(login_url='login')
def TipsPage(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    income_sum = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
    expense_sum = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
    print(income_sum)
    print(expense_sum)
    tip1 = ""
    tip2 = ""
    tip3 = ""
    tip4 = ""
    tip5 = ""
    tip6 = ""

    # Tip 1: Check if expenses are greater than income
    if expense_sum > income_sum:
        tip1 = "You are spending more money than you are earning. Consider cutting back on your expenses."

    # Tip 2: Analyze your expenses by category
    expense_categories = Expense.objects.filter(user=user).values('source').annotate(total=Sum('amount')).order_by('-total')
    if expense_categories:
        highest_expense = expense_categories.first()
        tip2 = f"You are spending the most money on {highest_expense['source']}. Consider reducing your spending in this category."

    # Tip 3: Set a budget and track your spending
    if profile.money > 0:
        budget_percentage = round((expense_sum / profile.money) * 100, 2)
        if budget_percentage >= 50:
            tip3 = "You have spent more than 50% of your budget. Consider setting a more realistic budget and tracking your expenses."

    # Tip 4: Reduce impulse spending
    recent_expenses = Expense.objects.filter(user=user).order_by('-created_at')[:5]
    if all(expense.amount < 20 for expense in recent_expenses):
        tip4 = "You seem to be making a lot of small impulse purchases. Consider being more mindful of your spending and avoiding unnecessary purchases."

    # Tip 5: Avoid unnecessary subscriptions
    entertaiment = Expense.objects.filter(user=user, source='entertaiment').aggregate(Sum('amount'))['amount__sum']
    if entertaiment > 0:
        tip5 = "You are spending money on entertaiment. Consider evaluating which ones you really need and canceling the rest."

    # Tip 6: Shop around for better deals
    if expense_categories:
        lowest_expense = expense_categories.last()
        tip6 = f"You are spending the least money on {lowest_expense['source']}. Consider exploring other options to see if you can find better deals."

    return render(request, 'tips.html', {'tip1': tip1, 'tip2': tip2, 'tip3': tip3, 'tip4': tip4, 'tip5': tip5, 'tip6': tip6})

