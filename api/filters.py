from django_filters import rest_framework as filters

from api.models import Genre, Movie, Tag


class MovieFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tag__tag", label="Tag", queryset=Tag.objects.all(), conjoined=True
    )

    class Meta:
        model = Movie
        fields = "__all__"


class TagFilter(filters.FilterSet):
    class Meta:
        model = Tag
        fields = "__all__"


class GenreFilter(filters.FilterSet):
    class Meta:
        model = Genre
        fields = "__all__"
