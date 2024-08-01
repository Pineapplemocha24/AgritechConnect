from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from .forms import *
from django.contrib import messages



#Login
def register_view(request):
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('login')
        else:
            msg = 'form is invalid' 
    else:
        form = RegisterForm()
    return render (request, 'register.html', {'form': form, 'msg': msg})   

def login_view(request):
    form = LoginForm(request.POST)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
            else: 
                msg = 'Invalid Login Credentials'
                
        else:
            msg = 'Error validating form'
    
    return render(request, 'login.html', {'form': form, 'msg': msg})
            