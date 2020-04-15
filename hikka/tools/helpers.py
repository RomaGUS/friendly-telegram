from hikka.services.descriptors import DescriptorService
from hikka.services.anime import AnimeService
from hikka.services.teams import TeamService
from hikka.services.users import UserService
from flask import abort as flask_abort
from hikka.errors import abort
from hikka.tools import check
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
    expression = r"[^@]+@[^@]+\.[^@]+"
    if not bool(re.search(expression, data)):
        response = abort("general", "not-found")
        flask_abort(response)

    return data

def image_link(data):
    # Based on
    # https://stackoverflow.com/a/51493215/9217774
    expression = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+(?:png|jpg|jpeg)+$"
    if not bool(re.search(expression, data)):
        response = abort("general", "not-file-link")
        flask_abort(response)

    return data

def anime(slug, account=None):
    anime = AnimeService.get_by_slug(slug)
    valid = False

    if anime:
        if anime.hidden is True:
            valid = check.member(account, anime.teams)
        else:
            valid = True

        if check.permission(account, "global", "admin"):
            valid = True

    if not valid:
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
    category = static.key("categories", slug)
    if not category:
        response = abort("category", "not-found")
        flask_abort(response)

    return category

def state(slug):
    state = static.key("states", slug)
    if not state:
        response = abort("state", "not-found")
        flask_abort(response)

    return state

def genre(slug):
    genre = static.key("genres", slug)
    if not genre:
        response = abort("genre", "not-found")
        flask_abort(response)

    return genre

def content(slug):
    content = static.key("content", slug)
    if not content:
        response = abort("content", "not-found")
        flask_abort(response)

    return content

def status(slug):
    status = static.key("statuses", slug)
    if not status:
        response = abort("status", "not-found")
        flask_abort(response)

    return status

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

def descriptor_service(slug):
    descriptor = static.key("descriptors", slug)
    if not descriptor:
        response = abort("descriptors", "not-found")
        flask_abort(response)

    return descriptor

def position(data):
    if data < 1:
        response = abort("general", "position-range")
        flask_abort(response)

    return data

def is_member(account, teams):
    if not check.member(account, teams):
        response = abort("account", "not-team-member")
        flask_abort(response)
