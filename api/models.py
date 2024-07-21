from django.db import models


class WeatherRequest(models.Model):
    """Модель запросов городов"""
    city = models.CharField(max_length=100)
