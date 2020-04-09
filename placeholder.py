from hikka.services.anime import AnimeService
from hikka.services.files import FileService
from hikka.tools import helpers
from jikanpy import Jikan
from hikka import utils
import requests

jikan = Jikan()
top = jikan.top(type="anime")

for index, item in enumerate(top["top"]):
    data = jikan.anime(item["mal_id"])
    myanimelist = data["mal_id"]

    if data["synopsis"] is None:
        data["synopsis"] = "Lorem ipsum dolor sit amet."

    title = AnimeService.get_title(data["title"])
    anime = AnimeService.create(
        title, data["synopsis"],
        helpers.category(data["type"].lower()),
        helpers.state("released"),
        utils.create_slug(data["title"])
    )

    anime.search = utils.create_search(anime.title.ua, data["title_synonyms"])
    anime.external = AnimeService.get_external(myanimelist)
    anime.year = data["aired"]["prop"]["from"]["year"]
    anime.teams = [helpers.team("fanvox")]
    anime.aliases = data["title_synonyms"]
    anime.total = data["episodes"]
    anime.rating = data["score"]

    for genre_data in data["genres"]:
        genre_slug = genre_data["name"].lower().replace("-", "_").replace(" ", "_")
        try:
            anime.genres.append(helpers.genre(genre_slug))
        except Exception:
            pass

    file = FileService.create(None, helpers.account("volbil"))
    file.path = data["image_url"]
    file.save()

    print(f"Saving {anime.title.ua}")
    anime["poster"] = file
    anime.save()

    if index > 40:
        break
