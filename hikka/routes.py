from hikka.modules import descriptors
from hikka.modules import releases
from hikka.modules import episodes
from hikka.modules import system
from hikka.modules import teams
from hikka.modules import auth
from hikka import api

# Auth routes
api.add_resource(auth.Join, "/auth/join")
api.add_resource(auth.Login, "/auth/login")
api.add_resource(auth.Activate, "/auth/activate")

# Team routes
api.add_resource(teams.NewTeam, "/teams/new")
api.add_resource(teams.GetTeam, "/teams/get/<string:slug>")
api.add_resource(teams.AddMember, "/teams/member/add")
api.add_resource(teams.RemoveMember, "/teams/member/remove")

# Genre routes
api.add_resource(descriptors.NewDescriptor, "/descriptors/new")
api.add_resource(descriptors.UpdateDescriptor, "/descriptors/update")

# Release routes
api.add_resource(releases.NewRelease, "/releases/new")
api.add_resource(releases.GetRelease, "/releases/get/<string:slug>")
api.add_resource(releases.ReleasesList, "/releases")

api.add_resource(episodes.AddEpisode, "/episodes/add")
api.add_resource(episodes.UpdateEpisode, "/episodes/update")
api.add_resource(episodes.DeleteEpisode, "/episodes/delete")

api.add_resource(system.ManagePermissions, "/system/permissions/manage")
api.add_resource(system.UserPermissions, "/system/permissions/user")
