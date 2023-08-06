from base64 import b64encode
from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

from atoti_core import keyword_only_dataclass

from .auth import Auth
from .token_authentication import TokenAuthentication


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class BasicAuthentication(Auth):
    """:class:`atoti_query.Auth` relying on `basic authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`__.

    See also:
        :class:`atoti.BasicAuthenticationConfig`.
    """

    username: str
    password: str

    def __call__(self, url: str) -> Mapping[str, str]:
        return self._token_authentication(url)

    @cached_property
    def _token_authentication(self) -> TokenAuthentication:
        plain_credentials = f"{self.username}:{self.password}"
        token = str(b64encode(plain_credentials.encode("ascii")), "utf8")
        return TokenAuthentication(token=token, token_type="Basic")  # nosec B106
