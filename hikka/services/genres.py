from hikka.services.models.genre import Genre
from typing import List

class GenresService:
    @classmethod
    def create(cls, name: str, slug: str, description=None) -> Genre:
        genre = Genre(
            name=name,
            slug=slug,
            description=description
        )

        genre.save()
        return genre

    @classmethod
    def get_by_slug(cls, slug: str):
        genre = Genre.objects().filter(slug=slug).first()
        return genre

    @classmethod
    def list(cls, page=0, limit=10) -> List[Genre]:
        offset = page * limit
        genres = Genre.objects().filter().limit(limit).skip(offset)
        return list(genres)
