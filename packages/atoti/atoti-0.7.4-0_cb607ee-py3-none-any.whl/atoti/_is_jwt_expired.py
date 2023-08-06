import json
from base64 import b64decode
from datetime import timedelta
from time import time
from typing import Any, Dict


def _parse_jwt_claims(jwt: str, /) -> Dict[str, Any]:
    claims: Dict[str, Any] = json.loads(b64decode(jwt.split(".")[1]))
    return claims


def is_jwt_expired(jwt: str, /, *, margin: timedelta = timedelta(minutes=30)) -> bool:
    claims = _parse_jwt_claims(jwt)

    expiry = claims.get("exp")

    if expiry is None:
        return False

    now = time()
    return (now + margin.total_seconds()) > int(expiry)
