from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Movie, Tag, Genre
from api.serializers import MovieSerializer, TagSerializer, GenreSerializer

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
