from django.urls import path, include
from rest_framework import routers
from api.views import MovieViewSet, DbView

router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)

urlpatterns = [path("", include(router.urls)), path("db", DbView.as_view(), name="db")]
