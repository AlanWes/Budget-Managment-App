from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        c_password=request.POST.get('confirm_password')
        # Validation
        if password==c_password:
            if len(password) < 8:
                return render(request, 'register.html', {'error_message': 'Password must contain at least 8 characters.'})
            elif not any(char.isdigit() for char in password):
                return render(request, 'register.html', {'error_message': 'Password must contain at least one number.'})
            elif not any(char.isupper() for char in password):
                return render(request, 'register.html', {'error_message': 'Password must contain at least one uppercase character.'})
            else:
                my_user=User.objects.create_user(uname, email, password)
                my_user.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('login')
        else:
            return render(request, 'register.html', {'error_message': "Those passwords didn't match. Try again."})

    return render (request,'register.html')

def LoginPage(request):
    if request.method=='POST':
        return redirect('home')
    else:   
        return render (request,'login.html')