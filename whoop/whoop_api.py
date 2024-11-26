#!/usr/bin/env python

from .oauth2 import OAuth2Client

AUTHORIZATION_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
ACCESS_TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
WHOOPAPI_URL = "https://api.prod.whoop.com/developer/v1"


class Whoop(object):
    """Wrapper class for Whoop API"""

    def __init__(self, client_id, client_secret, redirect_url=None):
        if not client_id or not client_secret:
            raise ValueError("Client id and secret must be provided.")

        self.oauth = OAuth2Client(url=WHOOPAPI_URL,
                                  authorization_url=AUTHORIZATION_URL,
                                  access_token_url=ACCESS_TOKEN_URL,
                                  redirect_url=redirect_url,
                                  client_id=client_id,
                                  client_secret=client_secret)

    @property
    def authorization_url(self):
        """Get the authorization url for the client"""
        return self.oauth.get_authorization_url()

    def get_access_token(self, authorization_code):
        """Request access token for a team.

        :param authorization_code: authorization code received from authorization endpoint.
        """
        return self.oauth.get_access_token(authorization_code)
    
    def get_refresh_token(self, refresh_token):
        """Request refresh token for a team.

        :param refresh_token: refresh token received from authorization endpoint.
        """
        return self.oauth.get_access_token(refresh_token)

    def get_sleep(self, access_token, params=None):
        return self.oauth.get(params=params, endpoint='/activity/sleep', access_token=access_token)