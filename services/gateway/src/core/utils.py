from dzshop.enums import RoleType

from config       import gateway_config


def get_role_type(steam_id: str) -> RoleType:
    """get_role_type ..."""
    return RoleType.admin if steam_id in gateway_config.admins_id else RoleType.user
