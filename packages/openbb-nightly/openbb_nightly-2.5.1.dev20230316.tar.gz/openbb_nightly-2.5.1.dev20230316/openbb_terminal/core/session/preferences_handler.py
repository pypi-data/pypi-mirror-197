# IMPORTS STANDARD
import dataclasses
from pathlib import Path
from typing import Union

# IMPORTS THIRDPARTY
from dotenv import set_key

# IMPORTS INTERNAL
from openbb_terminal.core.config.paths import SETTINGS_ENV_FILE
from openbb_terminal.core.session.current_user import (
    get_current_user,
    is_local,
    set_current_user,
)
from openbb_terminal.core.session.hub_model import patch_user_configs


def set_preference(
    name: str,
    value: Union[bool, Path, str],
    login: bool = False,
):
    """Set preference

    Parameters
    ----------
    name : str
        Preference name
    value : Union[bool, Path, str]
        Preference value
    login : bool
        If the preference is set during login
    """

    current_user = get_current_user()
    sync_enabled = current_user.preferences.SYNC_ENABLED
    local_user = is_local()

    # Set preference in current user
    updated_preferences = dataclasses.replace(current_user.preferences, **{name: value})
    updated_user = dataclasses.replace(current_user, preferences=updated_preferences)
    set_current_user(updated_user)

    # Set preference in local env file
    if local_user:
        set_key(str(SETTINGS_ENV_FILE), "OPENBB_" + name, str(value))

    # Send preference to cloud
    if not login and not local_user and (sync_enabled or name == "SYNC_ENABLED"):
        patch_user_configs(
            key=name,
            value=str(value),
            type_="settings",
            auth_header=current_user.profile.get_auth_header(),
        )
