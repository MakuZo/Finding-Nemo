from rest_framework import viewsets
from rest_framework.response import Response

from api.filters import GenreFilter, MovieFilter, TagFilter
from api.models import Genre, Movie, Tag
from api.serializers import GenreSerializer, MovieSerializer, TagSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MovieFilter
    ordering_fields = '__all__'


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filterset_class = GenreFilter


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_class = TagFilter
