import os
import re
from pathlib import Path
from textwrap import dedent
from typing import Literal, Optional

from atoti_core import deprecated, get_env_flag

from ._license_key import ALL_SUPPORTED_LICENSE_KEY_ENV_VARS
from ._path_utils import get_atoti_home
from ._version import VERSION

EULA = (Path(__file__).parent / "LICENSE").read_text(encoding="utf8")

COPIED_EULA_PATH = get_atoti_home() / "LICENSE"
HIDE_EULA_MESSAGE_ENV_VAR = "ATOTI_HIDE_EULA_MESSAGE"


EULA_MESSAGE = dedent(
    f"""\
    Welcome to atoti {VERSION}!

    By using this community edition, you agree with the license available at https://docs.atoti.io/latest/eula.html.
    Browse the official documentation at https://docs.atoti.io.
    Join the community at https://www.atoti.io/register.

    atoti collects telemetry data, which is used to help understand how to improve the product.
    If you don't wish to send usage data, you can apply for an evaluation license at https://www.atoti.io/contact and then install the `atoti-plus` plugin.

    You can hide this message by setting the `{HIDE_EULA_MESSAGE_ENV_VAR}` environment variable to True."""
)


def hide_new_eula_message() -> None:
    """Copy the current end-user license agreement to atoti's home directory."""
    COPIED_EULA_PATH.parent.mkdir(parents=True, exist_ok=True)
    COPIED_EULA_PATH.write_text(EULA, encoding="utf8")


def hide_new_license_agreement_message() -> None:
    deprecated(
        f"`atoti.{hide_new_license_agreement_message.__name__}()` is deprecated, use `atoti.{hide_new_eula_message.__name__}()` instead."
    )


EULA_CHANGED_MESSAGE = dedent(
    f"""\
    Thanks for updating to atoti {VERSION}!

    The license agreement has changed, it's available at https://docs.atoti.io/latest/eula.html.

    You can hide this message by calling `atoti.{hide_new_eula_message.__name__}()`."""
)


def _get_eula_change() -> Optional[Literal["version-only", "other"]]:
    copied_eula = COPIED_EULA_PATH.read_text(encoding="utf8")

    if copied_eula == EULA:
        return None

    previous, new = (
        re.sub(r"(\d+\.\d+\.\d+(\.dev\d+)?|\s)", "", text).lower()
        for text in (copied_eula, EULA)
    )
    return "version-only" if previous == new else "other"


def print_eula_message() -> None:
    if any(os.environ.get(env_var) for env_var in ALL_SUPPORTED_LICENSE_KEY_ENV_VARS):
        # Assume that this is Atoti+ as soon as a license key environment variable is set.
        # The validity of the license key will be checked by each started Java process.
        return

    if get_env_flag(HIDE_EULA_MESSAGE_ENV_VAR):
        if COPIED_EULA_PATH.exists():
            eula_change = _get_eula_change()
            if eula_change == "other":
                print(EULA_CHANGED_MESSAGE)
            elif eula_change == "version-only":
                hide_new_eula_message()
        else:
            COPIED_EULA_PATH.parent.mkdir(parents=True, exist_ok=True)
            hide_new_eula_message()
    else:
        print(EULA_MESSAGE)
