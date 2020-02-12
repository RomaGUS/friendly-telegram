from hikka.modules import categories
from hikka.modules import releases
from hikka.modules import genres
from hikka.modules import states
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
api.add_resource(genres.NewGenre, "/genres/new")
api.add_resource(genres.UpdateGenre, "/genres/update")

# State routes
api.add_resource(states.NewState, "/states/new")
api.add_resource(states.UpdateState, "/states/update")

# Category routes
api.add_resource(categories.NewCategory, "/categories/new")
api.add_resource(categories.UpdateCategory, "/categories/update")

# Release routes
api.add_resource(releases.NewRelease, "/releases/new")
api.add_resource(releases.GetRelease, "/releases/get/<string:slug>")
