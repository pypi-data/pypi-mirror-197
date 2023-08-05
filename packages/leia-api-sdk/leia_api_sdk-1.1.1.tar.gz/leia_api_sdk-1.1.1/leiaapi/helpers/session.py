import logging
from typing import Optional

import leiaapi.generated.api_client
import leiaapi.generated.rest
from leiaapi.generated import ApiClient
from .scheduler import scheduled, Scheduler
from ..generated.api import ApplicationApi
from ..generated.models import Application, LoginBody, LoginToken

logger = logging.getLogger(__name__)

TIME_BETWEEN_TOKEN_UPDATE = 300

# this is the __call_api method
old__call_api = leiaapi.generated.api_client.ApiClient._ApiClient__call_api


def __call_api_with_auto_login(self, resource_path, method, path_params=None,
                  query_params=None, header_params=None, *args, **kwargs):
    try:
        return old__call_api(self, resource_path, method, path_params, query_params, header_params, *args, **kwargs)
    except leiaapi.generated.rest.ApiException as e:
        if resource_path == '/login':
            raise
        if e.status != 401 or 'token' not in header_params:
            # It's not a login error, we do not care for it
            # Or there is no token to send in the request, and we do not care either
            raise
        logger.info("Leia Token is invalid or non existent, trying to refresh it")
        SessionManager.DEFAULT_SESSION.login()

        header_params['token'] = SessionManager.DEFAULT_SESSION.token
        return old__call_api(self, resource_path, method, path_params, query_params, header_params, *args, **kwargs)

# We override the initial __call_api method to be able to automatically login if the token is not valid
leiaapi.generated.api_client.ApiClient._ApiClient__call_api = __call_api_with_auto_login


class SessionManager:
    DEFAULT_SESSION: 'SessionManager' = None

    def __init__(self, api_key: str, client: Optional[ApiClient] = ApiClient(), auto_update_token: bool = True):
        """
        Create a SessionManager to manage the session with Leia.io
        :param api_key: The API Key to connect to api.leia.io
        :param client: A ApiClient object configure with the information of the server
        :param auto_update_token: Set to False to not update the token validity automatically
        """
        super().__init__()
        self._api_key: str = api_key
        self._client: Optional[ApiClient] = client
        self._token: Optional[str] = None
        self._application_api: ApplicationApi = ApplicationApi(api_client=self.client)
        self._application: Optional[Application] = None
        self._scheduler: Optional[Scheduler] = None
        self._auto_update_token = auto_update_token

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value
        self._application_api = ApplicationApi(api_client=self.client)

    @property
    def token(self):
        return self._token

    @property
    def application_api(self):
        return self._application_api

    @property
    def application(self):
        return self._application

    @property
    def scheduler(self):
        return self._scheduler

    def set_as_default(self):
        SessionManager.DEFAULT_SESSION = self
        return self

    def login(self):
        login = self._application_api.login_application_post(LoginBody(api_key=self.api_key))
        self._application: Optional[Application] = login.application
        self._token: Optional[str] = login.token

        if self._auto_update_token:
            @scheduled(TIME_BETWEEN_TOKEN_UPDATE)
            def renew():
                self._application_api.who_am_i(token=self.token)

            self._scheduler = renew
        return self

    def logout(self):
        if self.scheduler is not None:
            self.scheduler.cancel()
        self._application_api.logout_application(self.token)
        self._token = None
        return self