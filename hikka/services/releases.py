from hikka.services.models.release import Release, Title, Episode
from hikka.services.models.descriptor import Descriptor
from hikka.services.files import FileService
from hikka.services.models.team import Team
from hikka.services.models.user import User
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
                search: str, category: Descriptor, state: Descriptor,
                genres=List[Descriptor], teams=[Team],
                subtitles=[User], voiceover=[User],
                aliases=[]) -> Release:

        release = Release(
            title=title,
            slug=slug,
            description=description,
            search=search,
            category=category,
            state=state,
            genres=genres,
            teams=teams,
            subtitles=subtitles,
            voiceover=voiceover,
            aliases=aliases
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

    @classmethod
    def search(cls, query, categories=[], genres=[],
                states=[], teams=[], page=0, limit=20) -> List[Release]:

        offset = page * limit
        releases = Release.objects(search__contains=query)

        if len(categories) > 0:
            releases = releases.filter(category__in=categories)

        if len(genres) > 0:
            releases = releases.filter(genres__in=genres)

        if len(states) > 0:
            releases = releases.filter(state__in=states)

        if len(teams) > 0:
            releases = releases.filter(teams__in=teams)

        releases = releases.limit(limit).skip(offset)
        return list(releases)
