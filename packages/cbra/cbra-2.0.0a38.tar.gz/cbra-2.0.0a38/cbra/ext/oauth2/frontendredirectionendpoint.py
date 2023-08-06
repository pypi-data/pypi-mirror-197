# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from headless.ext.oauth2.models import TokenResponse

import cbra.core as cbra
from .models import ManagedGrant
from .params import FrontendTokenResponse
from .tokenhandlerendpoint import TokenHandlerEndpoint


class FrontendRedirectionEndpoint(TokenHandlerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'bff.redirection'
    path: str = '/bff/callback'
    status_code: int = 303
    summary: str = 'Frontend Redirection Endpoint'
    token: TokenResponse = FrontendTokenResponse

    async def get(
        self,
        requested_scope: str | None = fastapi.Cookie(
            default=None,
            title="Scope",
            description=(
                "A space-separated list indicting the scope that was used to "
                "create the grant."
            ),
            alias='bff.scope'
        ),
    ) -> ManagedGrant:
        scope: set[str] = set() if requested_scope is None\
            else set(filter(bool, str.split(requested_scope, ' ')))
        if self.token.refresh_token is None:
            raise NotImplementedError
        grant = ManagedGrant(
            client_id=self.client.client_id,
            iss=self.client.issuer,
            refresh_token=self.token.refresh_token,
            scope=scope
        )
        await self.storage.persist(grant)
        self.delete_cookies()
        cbra.Endpoint.set_cookie(self, 'oauth2.phantom', grant.id)
        return grant