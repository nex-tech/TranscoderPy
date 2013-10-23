import requests
from exceptions import TranscoderResponseError
from utils import __version__


class HTTPBackend(object):
    def __init__(self,
                 base_url,
                 api_username,
                 api_key,
                 resource_name=None,
                 api_version=None,
                 test=False,
                 timeout=None,
                 proxies=None,
                 cert=None,
                 verify=None):

        self.base_url = base_url

        if resource_name:
            self.base_url = base_url + '%s/' % resource_name

        self.http = requests.Session()

        self.requests_params = {
            'timeout': timeout,
            'proxies': proxies,
            'cert': cert,
            'verify': verify
        }

        self.api_username = api_username
        self.api_key = api_key
        self.test = test
        self.api_version = api_version

        self.http.headers.update(self.headers)

    @property
    def headers(self):
        """ Returns default headers, by setting the Content-Type, Accepts,
        User-Agent and API Key headers. """

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'ApiKey %s:%s' % (self.api_username, self.api_key),
            'User-Agent': 'transcoder-py v{0}'.format(__version__)
        }

        return headers


    def get(self, url, data=None):
        response = self.http.get(url, params=data)
        return self.process(response)


    def post(self, url, body=None):
        response = self.http.post(url, headers=self.headers, data=body, **self.requests_params)
        return self.process(response)


    def process(self, response):
        try:
            code = response.status_code

            if code == 204:
                body = None
            elif code == 402:
                body = {
                    "message": "Error",
                    "status": "error"
                }
            else:
                body = response.json()

            return Response(code, body, response.content, response)

        except ValueError:
            raise TranscoderResponseError(response, response.content)



class Response(object):
    def __init__(self, code, body, raw_body, raw_response):
        self.code = code
        self.body = body
        self.raw_body = raw_body
        self.raw_response = raw_response