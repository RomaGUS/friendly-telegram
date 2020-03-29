from hikka.services.models.anime import Anime, Title, Episode, External
from hikka.services.models.descriptor import Descriptor
from hikka.services.models.team import Team
from hikka.services.models.user import User
from hikka.services.models.file import File
from typing import List

class AnimeService:
    @classmethod
    def get_title(cls, ua: str, jp=None):
        title = Title(ua=ua, jp=jp)
        return title

    @classmethod
    def get_external(cls, mal):
        external = External(mal=mal)
        return external

    @classmethod
    def get_episode(cls, name: str, position: int, video: File):
        episode = Episode(name=name, position=position, video=video)
        return episode

    @classmethod
    def create(cls, title: Title, slug: str, description: str,
                year: int, total: int, search: str, category: Descriptor,
                state: Descriptor, external: External, genres=List[Descriptor], franchises=List[Descriptor],
                teams=[Team], subtitles=[User], voiceover=[User],
                aliases=[]) -> Anime:

        anime = Anime(
            title=title,
            slug=slug,
            description=description,
            year=year,
            total=total,
            search=search,
            category=category,
            state=state,
            genres=genres,
            franchises=franchises,
            teams=teams,
            subtitles=subtitles,
            voiceover=voiceover,
            external=external,
            aliases=aliases
        )

        anime.save()
        return anime

    @classmethod
    def add_episode(cls, anime: Anime, episode: Episode):
        anime.episodes.append(episode)
        anime.save()

    @classmethod
    def remove_episode(cls, anime: Anime, episode: Episode):
        if episode in anime.episodes:
            index = anime.episodes.index(episode)
            anime.episodes.pop(index)

        anime.save()

    @classmethod
    def find_position(cls, anime: Anime, position: int):
        episode = None
        for anime_episode in anime.episodes:
            if anime_episode.position == position:
                episode = anime_episode

        return episode

    @classmethod
    def get_by_slug(cls, slug: str):
        anime = Anime.objects().filter(slug=slug).first()
        return anime

    @classmethod
    def list(cls, page=0, limit=20) -> List[Anime]:
        offset = page * limit
        anime = Anime.objects().filter().limit(limit).skip(offset)
        return list(anime)

    @classmethod
    def years(cls) -> dict:
        data = list(
            Anime.objects().aggregate({
                "$group": {
                    "_id": "$total",
                    "min": {"$min": "$year"},
                    "max": {"$max": "$year"}
                }
            })
        )

        return {
            "min": data[0]["min"],
            "max": data[0]["max"]
        }

    @classmethod
    def search(cls, query, year: dict, categories=[], genres=[], franchises=[],
                states=[], teams=[], selected=False, page=0, limit=20) -> List[Anime]:

        offset = page * limit
        anime = Anime.objects(search__contains=query)

        if len(categories) > 0:
            anime = anime.filter(category__in=categories)

        if len(genres) > 0:
            anime = anime.filter(genres__all=genres)

        if len(franchises) > 0:
            anime = anime.filter(franchises__all=franchises)

        if len(states) > 0:
            anime = anime.filter(state__in=states)

        if len(teams) > 0:
            anime = anime.filter(teams__in=teams)

        if year["min"]:
            anime = anime.filter(year__gte=year["min"])

        if year["max"]:
            anime = anime.filter(year__lte=year["max"])

        anime = anime.limit(limit).skip(offset)
        return list(anime)

    @classmethod
    def selected(cls) -> List[Anime]:
        anime = Anime.objects(selected=True).filter()
        return list(anime)
