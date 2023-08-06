import urllib.request
import urllib.parse
import json

class HttpApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, path, data=None):
        url = urllib.parse.urljoin(self.base_url, path)
        headers = {'Content-Type': 'application/json'}
        if data:
            data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def get(self, path):
        return self._make_request('GET', path)

    def post(self, path, data=None):
        return self._make_request('POST', path, data)

    def put(self, path, data=None):
        return self._make_request('PUT', path, data)

    def patch(self, path, data=None):
        return self._make_request('PATCH', path, data)

    def delete(self, path):
        return self._make_request('DELETE', path)
