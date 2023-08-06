# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.types import NotFound
from cbra.types import SessionRequestPrincipal
from .endpoint import AuthorizationServerEndpoint
from .models import AuthorizationRequest
from .models import CurrentAuthorizationRequest
from .types import AuthorizationRequestIdentifier


class AuthorizationRequestEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'oauth2.authorize'
    principal: SessionRequestPrincipal # type: ignore
    path: str = '/requests'
    request_id: AuthorizationRequestIdentifier = fastapi.Cookie(
        default=...,
        title="Request ID",
        alias='oauth2.request',
        description=(
            "The authorization request identifier. This cookie is set by the "
            "authorization endpoint in the case that the resource owner "
            "needs to perform a certain action."
        )
    )
    summary: str = 'Authorization Request'

    async def get(self) -> CurrentAuthorizationRequest:
        request = await self.storage.get(AuthorizationRequest, self.request_id)
        if request is None:
            raise NotFound
        return CurrentAuthorizationRequest(
            client=request.client_info
        )