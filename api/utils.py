import re
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd
from django.conf import settings
from django.core.management import call_command
from django.db import transaction

from api.models import Genre, Movie, Tag

IMDB_URL = r"https://www.imdb.com/title/tt{}/"
DATASET_URL = r"http://files.grouplens.org/datasets/movielens/{}.zip"
TEMP_PATH = Path(settings.BASE_DIR) / ".temp"
ZIP_PATH = TEMP_PATH / "data.zip"


def load_dataset(dataset: str):
    """Clears the database and loads a new dataset into it.
    
    Args:
        dataset: name of movielens dataset
    """
    call_command("flush", verbosity=0, interactive=False)  # Clears the database
    try:
        dataset_path = _download_dataset(dataset)  # Downloads datased
        _insert_movies_from_dataset(_merge_datasheets(dataset_path))
        _insert_tags_from_path(dataset_path)
    except:
        shutil.rmtree(TEMP_PATH)
        raise
    shutil.rmtree(TEMP_PATH)  # Delete .temp directory


def _merge_datasheets(path: str) -> pd.DataFrame:
    """Merges movies, ratings and links into one datasheet
    
    Args:
        path: path to directory with dataset
    Returns:
        pandas.DataFrame with merged datasheets
    """
    movies_path = path / "movies.csv"
    ratings_path = path / "ratings.csv"
    links_path = path / "links.csv"

    ratings = pd.read_csv(ratings_path).groupby("movieId").mean().round(1)
    links = pd.read_csv(links_path, converters={"imdbId": lambda x: str(x)})[
        ["movieId", "imdbId"]
    ]
    movies = pd.read_csv(movies_path).merge(links, how="left", on="movieId")
    movies = movies.merge(ratings, how="left", on="movieId")
    return movies


def _insert_movies_from_dataset(dataset: pd.DataFrame):
    """Inserts merged dataset into database.

    Args:
        dataset: merged datasheets from movie lens dataset
    """
    # Store movies in a list to bulk create them
    # Storing genres as an attribute will allow
    # later to create them in bulk
    year_re = re.compile(r"\s\((\d\d\d\d)\)")
    movies_to_create = []
    for row in dataset.itertuples(index=False):
        title = year_re.sub("", row.title)
        year = year_re.search(row.title)
        if year:
            year = year.group(1)
        movie = Movie(
            id=row.movieId,
            title=title,
            year=year,
            score=row.rating,
            link=IMDB_URL.format(row.imdbId),
        )
        movie._genres = row.genres
        movies_to_create.append(movie)
    Movie.objects.bulk_create(movies_to_create)

    # Bulk create M2M to improve performance
    # See https://stackoverflow.com/a/10116452/9682496 for reference
    ThroughModel = Movie.genres.through
    genres = {}
    genres_to_add = []
    with transaction.atomic():
        for movie in movies_to_create:
            for genre in movie._genres.split("|"):
                if not genre in genres:
                    genres[genre] = Genre.objects.create(name=genre)
                genres_to_add.append(
                    ThroughModel(movie_id=movie.id, genre_id=genres[genre].id)
                )
    ThroughModel.objects.bulk_create(genres_to_add)


def _insert_tags_from_path(path: str):
    """Inserts tags from dataset into database
    
    Args:
        path: path to the dataset directory
    """
    tags_to_create = []
    df = pd.read_csv(path / "tags.csv")[["movieId", "tag"]]
    for row in df.itertuples(index=False):
        tags_to_create.append(Tag(movie_id=row[0], tag=row[1]))
    Tag.objects.bulk_create(tags_to_create)


def _download_dataset(dataset: str) -> str:
    """Downloads a dataset and extracts it into .temp directory.

    Returns a path to dataset.
    """
    TEMP_PATH.mkdir()
    urlretrieve(DATASET_URL.format(dataset), ZIP_PATH)
    with ZipFile(ZIP_PATH) as f:
        f.extractall(TEMP_PATH)
    ZIP_PATH.unlink()
    return TEMP_PATH / dataset
