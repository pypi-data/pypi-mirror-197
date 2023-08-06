from odoo.tests.common import HttpCase
from odoo.tools import config
import secrets
import json

HOST = "127.0.0.1"
PORT = config["http_port"]

class CommonCase(HttpCase):
    def setUp(self):
        super().setUp()
        self.api_key = self.env['auth.api.key'].create({
            'name': 'test api key',
            'key': secrets.token_hex(16),
            'user_id': self.env.ref('base.user_admin').id
        }).key

    def http(self, method, url, data=None, headers=None, timeout=10):
        self.env['base'].flush()
        if url.startswith('/'):
            url = "http://%s:%s%s" % (HOST, PORT, url)

        headers['content-type'] = 'application/json'

        if method == 'GET':
            return self.opener.get(url, timeout=timeout, headers=headers)
        elif method == 'POST':
            return self.opener.post(url, data=json.dumps(data), timeout=timeout, headers=headers)
        elif method == 'PUT':
            return self.opener.put(url, data=json.dumps(data), timeout=timeout, headers=headers)
