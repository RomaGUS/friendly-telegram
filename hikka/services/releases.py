from hikka.services.models.release import Release, Title
from hikka.services.models.type import ReleaseType
from typing import List

class ReleasesService:
    @classmethod
    def get_title(cls, ua: str, jp=None):
        title = Title(ua=ua, jp=jp)
        return title

    @classmethod
    def create(cls, title: Title, slug: str, description: str,
                rtype: ReleaseType, genres=[], teams=[]) -> Release:

        release = Release(
            title=title,
            slug=slug,
            description=description,
            rtype=rtype,
            genres=genres,
            teams=teams
        )

        release.save()
        return release

    @classmethod
    def get_by_slug(cls, slug: str):
        release = Release.objects().filter(slug=slug).first()
        return release

    @classmethod
    def list(cls, page=0, limit=10) -> List[Release]:
        offset = page * limit
        releases = Release.objects().filter().limit(limit).skip(offset)
        return list(releases)
