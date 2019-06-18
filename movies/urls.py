from django.urls import path, include
from rest_framework import routers
from api.views import MovieViewSet, TagViewSet, GenreViewSet, DbView

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'tags', TagViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('db', DbView.as_view()),
]
