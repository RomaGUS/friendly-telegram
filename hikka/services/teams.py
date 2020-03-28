from hikka.services.func import update_document
from hikka.services.files import FileService
from hikka.services.models.user import User
from hikka.services.models.team import Team
from hikka.services.models.file import File
from typing import List

class TeamService:
    @classmethod
    def create(cls, name: str, slug: str, description: str) -> Team:
        team = Team(
            name=name,
            description=description,
            slug=slug
        )

        team.save()
        return team

    @classmethod
    def update(cls, team: Team, **kwargs):
        team = update_document(team, kwargs)
        team.save()

    @classmethod
    def get_by_slug(cls, slug: str, hidden=False):
        team = Team.objects().filter(slug=slug, hidden=hidden).first()
        return team

    @classmethod
    def add_member(cls, team: Team, user: User):
        if user not in team.members:
            team.members.append(user)

        team.save()

    @classmethod
    def remove_member(cls, team: Team, user: User):
        if user in team.members:
            index = team.members.index(user)
            team.members.pop(index)

        team.save()

    @classmethod
    def update_avatar(cls, team: Team, file: File):
        if team.avatar:
            FileService.destroy(team.avatar)

        team.avatar = file
        team.save()

        return team

    @classmethod
    def list(cls) -> List[Team]:
        teams = Team.objects().filter()
        return list(teams)

    @classmethod
    def delete(cls, team: Team, soft=True):
        if soft:
            team.hidden = True
            team.save()
        else:
            team.delete()
