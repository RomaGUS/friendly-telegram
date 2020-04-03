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
    if anime is None:
        response = abort("anime", "not-found")
        flask_abort(response)

    return anime

def franchise(slug):
    franchise = DescriptorService.get_by_slug("franchise", slug)
    if franchise is None:
        response = abort("franchise", "not-found")
        flask_abort(response)

    return franchise

def category(slug):
    category = DescriptorService.get_by_slug("category", slug)
    if category is None:
        response = abort("category", "not-found")
        flask_abort(response)

    return category

def state(slug):
    state = DescriptorService.get_by_slug("state", slug)
    if state is None:
        response = abort("state", "not-found")
        flask_abort(response)

    return state

def genre(slug):
    genre = static.get_key(static.genres, slug)
    if genre is None:
        response = abort("genre", "not-found")
        flask_abort(response)

    return genre

def account(username):
    account = UserService.get_by_username(username)
    if account is None:
        response = abort("account", "not-found")
        flask_abort(response)

    return account

def team(slug):
    team = TeamService.get_by_slug(slug)
    if team is None:
        response = abort("team", "not-found")
        flask_abort(response)

    return team
