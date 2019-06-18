from rest_framework import status, views, viewsets
from rest_framework.response import Response

from api.filters import GenreFilter, MovieFilter, TagFilter
from api.models import Genre, Movie, Tag
from api.serializers import GenreSerializer, MovieSerializer, TagSerializer
from api.utils import load_dataset


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movies
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MovieFilter
    ordering_fields = "__all__"


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


class DbView(views.APIView):
    """
    View to fetch and load movie lens dataset
    
    * Requires 'source' parameter in body with the name of dataset
    """

    def post(self, request, format="json"):
        dataset = request.data.get("source")
        if not dataset:
            return Response(
                {"error": "Source wasn't provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            load_dataset(dataset)
        except:
            return Response(
                {
                    "error": "Something went wrong. Did u provide a valid dataset name? Try again later."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Dataset loaded succesfully."})
