import requests

from flask.ext.classy import FlaskView, route
from flask import request

from app import app
from app.controller import RaisersEdgeSyncController


class LoginView(FlaskView):

    def __init__(self):
        self.controller = RaisersEdgeSyncController()

    @staticmethod
    def index(self):
        url = app.config['LOGIN_URL']
        r = requests.get(url, verify=False)
        # this returns a redirect (?) that we need to send to the browser.
        return r.text

    def callback(self):
        payload = {
            'client_id': app.config['APPLICATION_ID'],
            'client_secret': app.config['APPLICATION_SECRET'],
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': app.config['AUTH_REDIRECT_URL'],
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = app.config['TOKEN_URL']

        r = requests.post(url, data=payload, verify=False)
        json = r.json()

        resp = self.controller.add_tokens_to_database(json['access_token'], json['refresh_token'])
        return "Logged in at %s" % str(resp)

