from hikka.modules import releases
from hikka.modules import genres
from hikka.modules import types
from hikka.modules import teams
from hikka.modules import files
from hikka.modules import auth
from hikka import api

# Auth routes
api.add_resource(auth.Join, "/auth/join")
api.add_resource(auth.Login, "/auth/login")
api.add_resource(auth.Activate, "/auth/activate")

# Team routes
api.add_resource(teams.NewTeam, "/teams/new")

# Genre routes
api.add_resource(genres.NewGenre, "/genres/new")
api.add_resource(genres.UpdateGenre, "/genres/update")

# Type routes
api.add_resource(types.NewReleaseType, "/types/new")
api.add_resource(types.UpdateReleaseType, "/types/update")

# Release routes
api.add_resource(releases.NewRelease, "/releases/new")

# Misc
api.add_resource(files.Upload, "/upload")
