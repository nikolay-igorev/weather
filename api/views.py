from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import WeatherRequest


"""View статистики запросов городов"""
@api_view()
def statistics(request):
    queryset = WeatherRequest.objects.values('city').annotate(count=Count('city')).filter(count__gt=0)
    return Response(queryset)
