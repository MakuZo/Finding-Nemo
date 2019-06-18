from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Movie


class MovieTests(APITestCase):
    fixtures = ["movies"]
    url = reverse("movie-list")

    def test_get_all_movies(self):
        """Ensure that all movies can be fetched"""
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], Movie.objects.count())

    def test_get_one_movie(self):
        """Ensure that one movie can be fetched"""
        url = reverse("movie-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.data["title"], Movie.objects.get(pk=1).title)

    def test_filter_by_year(self):
        """Ensure that movies can be filtered by year"""
        response = self.client.get(self.url, {"year": 1995})
        self.assertEqual(
            response.data["count"], Movie.objects.filter(year=1995).count()
        )

    def test_order_by_year(self):
        """Ensure that movies can be ordered by year"""
        response = self.client.get(self.url, {"sort": "-year"})
        self.assertEqual(
            response.data["results"][0]["year"], Movie.objects.order_by("-year")[0].year
        )

    def test_field_order_matches_task_specification(self):
        """Ensure that serializer returns fields in order that matches task specification"""
        url = reverse("movie-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertListEqual(
            list(response.data.keys()), ["title", "score", "genres", "link", "year"]
        )

    def test_filter_by_tag(self):
        """Ensure that movies can be filtered by tag"""
        response = self.client.get(self.url, {"tag": ["fun", "pixar"]})
        self.assertEqual(
            response.data["results"][0]["title"],
            Movie.objects.filter(tag__tag="fun")
            .filter(tag__tag="pixar")
            .first()
            .title,
        )


class DbTests(APITestCase):
    url = reverse("db")

    def test_load_small_dataset(self):
        """Ensure that small dataset can be loaded"""
        response = self.client.post(self.url, {"source": "ml-latest-small"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_400_when_invalid_source(self):
        """Ensure view returns HTTP400 when passing invalid dataset name"""
        response = self.client.post(self.url, {"source": "invalid-name"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_400_when_blank_source(self):
        """Ensure view returns HTTP400 when passing blank dataset name"""
        response = self.client.post(self.url, {"source": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_400_when_blank_form(self):
        """Ensure view returns HTTP400 when passing blank form"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
