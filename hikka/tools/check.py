from hikka.services.permissions import PermissionService

def permission(account, scope, message):
    return PermissionService.check(account, scope, message)

def member(account, teams):
    member = False

    for team in teams:
        if account in team.members:
            member = True

    return member
