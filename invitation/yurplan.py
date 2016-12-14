import json

import requests
from django.conf import settings


class ApiClient:
    _AUTH_TOKEN = ""

    @staticmethod
    def _authenticate():
        auth_request = requests.post('https://api.yurplan.com/v1/token', data={
            'grant_type': 'client_credentials',
            'scope': 'pro',
            'client_id': settings.YURPLAN_APP_ID,
            'client_secret': settings.YURPLAN_APP_SECRET,
        })
        auth = json.loads(auth_request.text)
        if auth['status'] == 200:
            ApiClient._AUTH_TOKEN = auth['results']['access_token']
            return True
        else:
            return False

    def get_event(self, try_auth=True):
        r = requests.get('https://api.yurplan.com/v1/events/{}'.format(settings.YURPLAN_EVENT_ID), headers={
            'Authorization': 'Bearer {}'.format(ApiClient._AUTH_TOKEN)
        })
        if r.status_code == 200:
            return json.loads(r.text)['results']
        else:
            if try_auth and r.status_code != 404:
                ApiClient._authenticate()
                return self.get_event(try_auth=False)
            else:
                return None

    def get_order(self, order_id, try_auth=True):
        r = requests.get('https://api.yurplan.com/v1/events/{}/orders/{}'.format(settings.YURPLAN_EVENT_ID, order_id),
                         headers={
                             'Authorization': 'Bearer {}'.format(ApiClient._AUTH_TOKEN)
                         })
        if r.status_code == 200:
            return json.loads(r.text)['results']
        else:
            if try_auth and r.status_code != 404:
                ApiClient._authenticate()
                return self.get_order(order_id, try_auth=False)
            else:
                return None
