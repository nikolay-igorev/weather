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

        for response in response.data:
            if response['city'] == 'Krasnoyarsk':
                self.assertEqual(response['count'], self.krasnoyarsk_count)
            elif response['city'] == 'London':
                self.assertEqual(response['count'], self.london_count)
            elif response['city'] == 'New York':
                self.assertEqual(response['count'], self.new_york_count)
