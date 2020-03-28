from hikka.services.descriptors import DescriptorService
from hikka.services.anime import AnimeService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from hikka.errors import abort
import re

from flask_restful import abort as flask_abort

def string(data):
    if not data:
        abort("general", "empty-string")

    return data

def email(data):
    if not bool(re.search(r"[^@]+@[^@]+\.[^@]+", data)):
        abort("general", "invalid-email")

    return data

def anime(slug):
    anime = AnimeService.get_by_slug(slug)
    if anime is None:
        abort("anime", "not-found")

    return anime

def franchise(slug):
    franchise = DescriptorService.get_by_slug("franchise", slug)
    if franchise is None:
        abort("franchise", "not-found")

    return franchise

def category(slug):
    category = DescriptorService.get_by_slug("category", slug)
    if category is None:
        abort("category", "not-found")

    return category

def state(slug):
    state = DescriptorService.get_by_slug("state", slug)
    if state is None:
        abort("state", "not-found")

    return state

def genre(slug):
    genre = DescriptorService.get_by_slug("genre", slug)
    if genre is None:
        abort("genre", "not-found")

    return genre

def account(username):
    account = UserService.get_by_username(username)
    if account is None:
        abort("account", "not-found")

    return account

def team(slug):
    team = TeamService.get_by_slug(slug)
    if team is None:
        # abort("team", "not-found")
        flask_abort(422)

    return team
