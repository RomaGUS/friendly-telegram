from hikka.services.permissions import PermissionsService
from hikka.services.users import UserService
import mongoengine
import config

db_settings = dict(
    username=config.db["username"],
    password=config.db["password"],
    port=config.db["port"]
)

mongoengine.register_connection(
    alias="default",
    name=config.db["name"],
    **db_settings
)

account = UserService.get_by_username("volbil")
PermissionsService.add(account, f"team-volbil", "admin")
