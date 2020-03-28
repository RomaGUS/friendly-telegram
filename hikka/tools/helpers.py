from hikka.services.descriptors import DescriptorService
from hikka.services.anime import AnimeService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from hikka.errors import abort
import re

def string(data):
    if not data:
        return abort("general", "empty-string")

    return data

def email(data):
    if not bool(re.search(r"[^@]+@[^@]+\.[^@]+", data)):
        return abort("general", "invalid-email")

    return data

def anime(slug):
    anime = AnimeService.get_by_slug(slug)
    if anime is None:
        return abort("anime", "not-found")

    return anime

def franchise(slug):
    franchise = DescriptorService.get_by_slug("franchise", slug)
    if franchise is None:
        return abort("franchise", "not-found")

    return franchise

def category(slug):
    category = DescriptorService.get_by_slug("category", slug)
    if category is None:
        return abort("category", "not-found")

    return category

def state(slug):
    state = DescriptorService.get_by_slug("state", slug)
    if state is None:
        return abort("state", "not-found")

    return state

def genre(slug):
    genre = DescriptorService.get_by_slug("genre", slug)
    if genre is None:
        return abort("genre", "not-found")

    return genre

def account(username):
    account = UserService.get_by_username(username)
    if account is None:
        return abort("account", "not-found")

    return account

def team(slug):
    team = TeamService.get_by_slug(slug)
    if team is None:
        return abort("team", "not-found")

    return team
