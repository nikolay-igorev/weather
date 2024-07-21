from django import forms


class WeatherForm(forms.Form):
    """Форма для ввода города"""
    city = forms.CharField(max_length=100)
