from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
import requests
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect


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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect to the index page after login
                return redirect('index')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('index')

# Index


def index(request):
    return render(request, 'index.html')


def weather(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=34905b0a9f52a09e99ea72b2d1ea22a5"

    cities = City.objects.all()  # return all the cities in the database

    if request.method == 'POST':
        # add an actual request for the data to form the processing
        form = CityForm(request.POST)
        form.save()  # saves the form if valid
    form = CityForm()

    weather_data = []

    for city in cities:
        # request the API data and convert the JSON to Python data types
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        # add the data for the current city to our list
        weather_data.append(weather)

    context = {
        'weather_data': weather_data,
        'form': form
    }
    
    # print(city_weather) -- to test the API key
    return render(request, 'weather.html', context)


def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect('weather')
