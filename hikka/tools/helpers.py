from hikka.services.descriptors import DescriptorService
from hikka.services.anime import AnimeService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from flask import abort as flask_abort
from hikka.errors import abort
from hikka import static
import re

def string(data):
    if not data:
        response = abort("general", "not-found")
        flask_abort(response)

    return data

def password(data):
    if len(data) < 8 or len(data) > 32:
        response = abort("general", "password-length")
        flask_abort(response)

    return data

def email(data):
    if not bool(re.search(r"[^@]+@[^@]+\.[^@]+", data)):
        response = abort("general", "not-found")
        flask_abort(response)

    return data

def anime(slug):
    anime = AnimeService.get_by_slug(slug)
    if not anime:
        response = abort("anime", "not-found")
        flask_abort(response)

    return anime

def franchise(slug):
    franchise = DescriptorService.get_by_slug("franchise", slug)
    if not franchise:
        response = abort("franchise", "not-found")
        flask_abort(response)

    return franchise

def category(slug):
    category = static.get_key("categories", slug)
    if not category:
        response = abort("category", "not-found")
        flask_abort(response)

    return category

def state(slug):
    state = static.get_key("states", slug)
    if not state:
        response = abort("state", "not-found")
        flask_abort(response)

    return state

def genre(slug):
    genre = static.get_key("genres", slug)
    if not genre:
        response = abort("genre", "not-found")
        flask_abort(response)

    return genre

def account(username):
    account = UserService.get_by_username(username)
    if not account:
        response = abort("account", "not-found")
        flask_abort(response)

    return account

def team(slug):
    team = TeamService.get_by_slug(slug)
    if not team:
        response = abort("team", "not-found")
        flask_abort(response)

    return team
