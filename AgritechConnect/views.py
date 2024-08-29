from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
import requests
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ForumPostForm, CommentForm

from .models import City
from .forms import RegisterForm, LoginForm, CityForm

# Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            farmer = form.save(commit=False)
            farmer.save()
            return redirect('login')
        else:
            print(form.errors)  # Print form errors to debug
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)  # Pass 'request' as the first argument
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Logout
def logout(request):
    auth_logout(request)
    return redirect('index')

# Index
def index(request):
    return render(request, 'index.html')

# Contact


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Process the form data (e.g., send an email)
        send_mail(
            subject,
            message,
            email,  # From email
            ['info@agritechconnect.com'],  # To email
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')


# Messages
def messages_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
 
    return render(request, 'messages.html')

# Weather
def weather(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=34905b0a9f52a09e99ea72b2d1ea22a5"

    cities = City.objects.all()  # Return all the cities in the database

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form if valid
            return redirect('weather')
    else:
        form = CityForm()

    weather_data = []

    for city in cities:
        # Request the API data and convert the JSON to Python data types
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    context = {
        'weather_data': weather_data,
        'form': form
    }
    
    return render(request, 'weather.html', context)

# Delete City
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect('weather')


def forum_list(request):
    posts = ForumPost.objects.all().order_by('-created_at')
    return render(request, 'forum_list.html', {'posts': posts})

def forum_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('forum_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'forum_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum_list')
    else:
        form = ForumPostForm()

    return render(request, 'create_post.html', {'form': form})

def best_practices(request):
    videos = BestPracticeVideo.objects.all()
    return render(request, 'best_practices.html', {'videos': videos})


def market_info(request):
    # Sample static data, replace with dynamic content if needed
    market_data = {
        'title': 'Market Information',
        'introduction': 'Stay updated with the latest market trends and prices to make informed decisions.',
        'sections': [
            {
                'heading': 'Current Market Trends',
                'content': 'Here, we provide insights into the latest market trends affecting different crops and products.'
            },
            {
                'heading': 'Price Fluctuations',
                'content': 'Understand how prices are fluctuating in the market and what factors are influencing these changes.'
            },
            {
                'heading': 'Regional Market Insights',
                'content': 'Get insights into specific regional markets and how local factors are affecting prices and demand.'
            },
            {
                'heading': 'Tips for Farmers',
                'content': 'Learn practical tips and strategies to navigate the market effectively and maximize profits.'
            }
        ]
    }
    
    return render(request, 'market_info.html', {'market_data': market_data})



