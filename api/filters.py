from django_filters import rest_framework as filters

from api.models import Movie


class MovieFilter(filters.FilterSet):
    class Meta:
        model = Movie
        fields = ('year',)
