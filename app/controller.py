import requests
from datetime import datetime

from db import connect_to_db

from app import app


class RaisersEdgeSyncController(object):

    def __init__(self, route_prefix=''):
        self.db = connect_to_db()
        self.login_table = self.db[app.config['LOGIN_TABLE']]

        self.route_prefix = route_prefix


    def call_api(self, route):
        # get_access_token()
        url = app.config['API_URL']
        url %= (self.route_prefix, route)
        access_token, refresh_token = self.get_tokens()
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'bb-api-subscription-key': app.config['SUBSCRIPTION_KEY'],
            'Authorization': 'Bearer %s' % access_token
        }

        r = requests.get(url, headers=headers)
        return r.json()

    def add_tokens_to_database(self, access_token, refresh_token):
        now = datetime.today()
        data = dict(access_token=access_token, refresh_token=refresh_token, timestamp=now)
        return self.login_table.upsert(data, ['timestamp'])

    def get_tokens(self):
        row = self.login_table.find_one(order_by=['-timestamp'])
        return row['access_token'], row['refresh_token']

    def refresh_token(self):
        # get new Access Token from Blackbaud, store in DB and also in Class context

        access_token, refresh_token = self.get_tokens()

        payload = {
            'client_id': app.config['APPLICATION_ID'],
            'client_secret': app.config['APPLICATION_SECRET'],
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = app.config['TOKEN_URL']

        r = requests.post(url, data=payload, verify=False)
        json = r.json()

        self.add_tokens_to_database(json['access_token'], json['refresh_token'])