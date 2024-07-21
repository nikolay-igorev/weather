from django.test import TestCase
from .models import WeatherRequest


class WeatherRequestTestCase(TestCase):
    def setUp(self):
        WeatherRequest.objects.create(city='Krasnoyarsk')
        WeatherRequest.objects.create(city='Krasnoyarsk')

        WeatherRequest.objects.create(city='London')
        WeatherRequest.objects.create(city='London')
        WeatherRequest.objects.create(city='London')

        WeatherRequest.objects.create(city='New York')

        self.krasnoyarsk_count = WeatherRequest.objects.filter(city='Krasnoyarsk').count()
        self.london_count = WeatherRequest.objects.filter(city='London').count()
        self.new_york_count = WeatherRequest.objects.filter(city='New York').count()

    def test_weather_request_count(self):
        response = self.client.get('/api/statistics/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['count'], self.krasnoyarsk_count)
        self.assertEqual(response.data[1]['count'], self.london_count)
        self.assertEqual(response.data[2]['count'], self.new_york_count)
