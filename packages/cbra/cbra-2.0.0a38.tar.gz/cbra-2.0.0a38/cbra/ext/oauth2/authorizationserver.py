# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from fastapi.responses import RedirectResponse

import cbra.core as cbra
from cbra.core.conf import settings
from cbra.types import Request
from .applicationstorage import ApplicationStorage
from .authorizationendpoint import AuthorizationEndpoint
from .authorizationrequestendpoint import AuthorizationRequestEndpoint
from .authorizationserverstorage import AuthorizationServerStorage
from .callbackendpoint import CallbackEndpoint
from .currentsubjectendpoint import CurrentSubjectEndpoint
from .endpoint import AuthorizationServerEndpoint
from .frontendloginendpoint import FrontendLoginEndpoint
from .frontendredirectionendpoint import FrontendRedirectionEndpoint
from .metadataendpoint import MetadataEndpoint
from .onboardingendpoint import OnboardingEndpoint
from .tokenendpoint import TokenEndpoint
from .tokenhandlerendpoint import TokenHandlerEndpoint
from .types import ResponseType


class AuthorizationServer(cbra.APIRouter):
    __module__: str = 'cbra.ext.oauth2'
    client: dict[str, Any] | None | bool
    downstream: dict[str, Any] | None
    iss: str | None
    handlers: set[type[AuthorizationServerEndpoint | TokenHandlerEndpoint]] = set()
    response_types: list[ResponseType]
    storage_class: type[AuthorizationServerStorage]

    def __init__(
        self,
        response_types: list[ResponseType] | None,
        iss: str | None = None,
        client: dict[str, Any] | None | bool = None,
        downstream: dict[str, Any] | None = None,
        storage_class: type[AuthorizationServerStorage] = AuthorizationServerStorage,
        *args: Any,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs) # type: ignore
        self.client = client
        self.downstream = downstream
        self.iss = iss
        self.response_types = response_types or []
        self.storage_class = storage_class

        # Determine which request handlers we must add to the authorization
        # server.
        self.handlers = {
            AuthorizationRequestEndpoint,
            CurrentSubjectEndpoint,
            FrontendLoginEndpoint,
            FrontendRedirectionEndpoint,
            OnboardingEndpoint
        }

        # If there is any response type, this indicates that the
        # server must provide an authorization endpoint.
        if response_types:
            self.handlers.add(AuthorizationEndpoint)
            self.handlers.add(CallbackEndpoint)
            self.handlers.add(TokenEndpoint)

    def add_to_router(self, router: cbra.Application, *args: Any, **kwargs: Any):
        self.container = router.container
        self.container.provide('_LocalClient', {
            'qualname': '_',
            'symbol': self.get_local_client
        })
        self.container.provide('_ApplicationStorage', {
            'qualname': f'{ApplicationStorage.__module__}.{ApplicationStorage.__name__}',
            'symbol': ApplicationStorage
        })
        self.container.provide('_AuthorizationServerStorage', {
            'qualname': f'{self.storage_class.__module__}.{self.storage_class.__name__}',
            'symbol': self.storage_class
        })
        self.container.provide('AuthorizationServerStorage', {
            'qualname': settings.OAUTH2_STORAGE
        })
        for handler in sorted(self.handlers, key=lambda x: x.__name__):
            self.add(handler, path=handler.path)

        # The metadata endpoint is a special case - its always added
        # to the root application. Also add the metadata endpoint
        # to .well-known/openid-configuration for OIDC compatibility.
        router.add(MetadataEndpoint, path=MetadataEndpoint.path)
        router.add_api_route(
            path="/.well-known/openid-configuration",
            endpoint=self.redirect_metadata,
            include_in_schema=False,
        )

        return super().add_to_router(router, *args, **kwargs)

    def get_local_client(self, request: Request) -> dict[str, Any]:
        """Return the client that the authorization server uses to authenticate
        and authorize a subject for interaction with itself.
        """
        return {
            'allowed_redirect_uris': [
                str(request.url_for('bff.redirection'))
            ],
            'issuer': f'https://{request.url.netloc}',
            'client_id': 'self',
            'client_name': request.url.netloc,
            'client_secret': settings.SECRET_KEY,
            'downstream': {
                'required': bool(self.downstream),
                'providers': [self.downstream] if self.downstream else []
            },
            'grant_types': ['authorization_code'],
            'organization_name': "Molano B.V.",
            'refresh_token_ttl': 86400,
            'scope': {'email', 'openid', 'profile'},
            'sector_identifier': str(request.url.netloc),
            'token_endpoint_auth_method': 'client_secret_post'
        }

    async def redirect_metadata(self, request: Request) -> RedirectResponse:
        return RedirectResponse(
            status_code=303,
            url=request.url_for('oauth2.metadata')
        )