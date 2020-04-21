from hikka.services.models.anime import Anime, Title, Episode, External
from hikka.services.models.descriptor import Descriptor
from hikka.services.teams import TeamService
from mongoengine.queryset.visitor import Q
from typing import List

class AnimeService:
    @classmethod
    def get_title(cls, ua: str, jp=None):
        title = Title(ua=ua, jp=jp)
        return title

    @classmethod
    def get_external(cls, myanimelist=None, toloka=None):
        external = External(
            myanimelist=myanimelist,
            toloka=toloka
        )

        return external

    @classmethod
    def get_episode(cls, position: int):
        episode = Episode(position=position)
        return episode

    @classmethod
    def create(cls, title: Title, description: str,
                category: Descriptor, state: Descriptor,
                slug: str) -> Anime:

        anime = Anime(
            title=title,
            description=description,
            category=category,
            state=state,
            slug=slug
        )

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
    def position_index(cls, anime: Anime, position: int):
        for index, episode in enumerate(anime.episodes):
            if episode.position == position:
                return index

        return None

    @classmethod
    def get_by_slug(cls, slug: str):
        anime = Anime.objects().filter(slug=slug).first()
        return anime

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
            "min": data[0]["min"] if len(data) > 0 else None,
            "max": data[0]["max"] if len(data) > 0 else None
        }

    @classmethod
    def search(cls, query, year: dict, categories=[], genres=[],
                franchises=[], states=[], teams=[], ordering=[],
                selected=False, page=0, limit=20, account=None) -> List[Anime]:

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

        teams = TeamService.member_teams(account)
        anime = anime.filter(Q(hidden=False) | Q(teams__in=teams))

        if len(ordering) > 0:
            anime = anime.order_by(*ordering)

        anime = anime.limit(limit).skip(offset)

        return list(anime)

    @classmethod
    def selected(cls) -> List[Anime]:
        anime = Anime.objects(selected=True).filter()
        return list(anime)
