from rest_framework import serializers

from api.models import Movie, Tag, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        # Fields declared specifically to keep proper order
        # when rendering response
        fields = ('title', 'score', 'genres', 'link', 'year')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'