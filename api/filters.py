from django_filters import rest_framework as filters

from api.models import Movie, Tag


class MovieFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tag__tag", label="Tag", queryset=Tag.objects.all(), conjoined=True
    )

    class Meta:
        model = Movie
        fields = ('tag', 'year')
