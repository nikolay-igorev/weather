from django.test import TestCase, Client
from django.urls import reverse

from .views import get_weather
from api.models import WeatherRequest


class BlogTestCase(TestCase):
    def setUp(self):
        self.city = "London"
        self.wrong_city = 'ssssssssssssssssss'

    def test_weather_page(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(url, '/')

    def test_weather(self):
        url = reverse('index')

        response = self.client.post(url, {'city': self.city})
        temperature, precipitation = get_weather(self.city)
        weather_request_count = WeatherRequest.objects.filter(city=self.city).count()

        self.assertContains(response, self.city, status_code=200)
        self.assertContains(response, temperature, status_code=200)
        self.assertContains(response, precipitation, status_code=200)
        self.assertEqual(weather_request_count, 1)

    def test_wrong_weather(self):
        url = reverse('index')

        response = self.client.post(url, {'city': self.wrong_city})
        weather_request_count = WeatherRequest.objects.filter(city=self.city).count()

        self.assertContains(response, 'wrong city name', status_code=200)
        self.assertEqual(weather_request_count, 0)
