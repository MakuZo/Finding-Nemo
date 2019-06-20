from rest_framework import status, views, viewsets
from rest_framework.response import Response

from api.filters import MovieFilter
from api.models import Movie
from api.serializers import MovieSerializer
from api.utils import load_dataset


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movies
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MovieFilter
    ordering_fields = ("year",)

    def filter_queryset(self, queryset):
        """
        Returns filtered queryset.

        Sadly django-filters doesn't support AND syntax in queries (for CharFilter).

        ModelMultipleChoiceFilter behaves buggy when e.g. filtering by one tag.
        Also, it would require writing custom form to 'accept' invalid tag names
        and return empty queryset.

        Filtering by tag is done in a view to spare the pain.
        """
        tags = self.request.GET.getlist("tag")
        if tags:
            for tag in tags:
                queryset = queryset.filter(tag__tag=tag)
        return super().filter_queryset(queryset)


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
