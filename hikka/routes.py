from hikka.modules import descriptors
from hikka.modules import releases
from hikka.modules import teams
from hikka.modules import auth
from hikka import api

# Auth routes
api.add_resource(auth.Join, "/auth/join")
api.add_resource(auth.Login, "/auth/login")
api.add_resource(auth.Activate, "/auth/activate")
api.add_resource(auth.Test, "/auth/test")

# Team routes
api.add_resource(teams.NewTeam, "/teams/new")

# Genre routes
api.add_resource(descriptors.NewDescriptor, "/descriptors/new")
api.add_resource(descriptors.UpdateDescriptor, "/descriptors/update")

# Release routes
api.add_resource(releases.NewRelease, "/releases/new")
api.add_resource(releases.GetRelease, "/releases/get/<string:slug>")
