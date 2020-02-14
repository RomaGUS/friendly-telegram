from hikka.services.models.release import Release, Title, Episode
from hikka.services.models.category import Category
from hikka.services.models.state import State
from hikka.services.files import FileService
from hikka.services.models.file import File
from typing import List

class ReleaseService:
    @classmethod
    def get_title(cls, ua: str, jp=None):
        title = Title(ua=ua, jp=jp)
        return title

    @classmethod
    def get_episode(cls, name: str, position: int, video: File):
        episode = Episode(name=name, position=position, video=video)
        return episode

    @classmethod
    def create(cls, title: Title, slug: str, description: str,
                category: Category, state: State,
                genres=[], teams=[], subtitles=[],
                voiceover=[]) -> Release:

        release = Release(
            title=title,
            slug=slug,
            description=description,
            category=category,
            state=state,
            genres=genres,
            teams=teams,
            subtitles=subtitles,
            voiceover=voiceover
        )

        release.save()
        return release

    @classmethod
    def update_poster(cls, release: Release, file: File):
        if release.poster is not None:
            FileService.destroy(release.poster)

        release.poster = file
        release.save()

        return release

    @classmethod
    def add_episode(cls, release: Release, episode: Episode):
        release.episodes.append(episode)
        release.save()

    @classmethod
    def remove_episode(cls, release: Release, episode: Episode):
        if episode in release.episodes:
            index = release.episodes.index(episode)
            release.episodes.pop(index)

        release.save()

    @classmethod
    def find_position(cls, release: Release, position: int):
        episode = None
        for release_episode in release.episodes:
            if release_episode.position == position:
                episode = release_episode

        return episode

    @classmethod
    def get_by_slug(cls, slug: str):
        release = Release.objects().filter(slug=slug).first()
        return release

    @classmethod
    def list(cls, page=0, limit=20) -> List[Release]:
        offset = page * limit
        releases = Release.objects().filter().limit(limit).skip(offset)
        return list(releases)
