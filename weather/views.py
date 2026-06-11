from django.shortcuts import render
from datetime import datetime
import requests

from .models import SearchHistory

API_KEY = "4cd6b6bcc34c1a2832c8af69a3bb78a3"


def home(request):

    weather_data = {}

    if request.method == "POST":

        city = request.POST.get('city')

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        print("STATUS:", response.status_code)
        print(data)

        if response.status_code == 200:

            SearchHistory.objects.create(city=city)

            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].title(),
                'wind': data['wind']['speed'],
                'icon': data['weather'][0]['icon'],
                'date': datetime.now().strftime("%d %B %Y"),
                'time': datetime.now().strftime("%I:%M %p")
            }

    history = SearchHistory.objects.all().order_by('-id')[:5]

    return render(
        request,
        'index.html',
        {
            'weather': weather_data,
            'history': history
        }
    )