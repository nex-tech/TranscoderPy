import requests
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

__version__ = '0.1'


class TranscoderError(Exception):
    pass


class TranscoderResponseError(Exception):
    def __init__(self, http_response, content):
        self.http_response = http_response
        self.content = content


class HTTPBackend(object):
    def __init__(self,
                 base_url,
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
            'Authorization': 'ApiKey agabel:%s' % self.api_key,
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



class Transcoder(object):

    def __init__(self, api_key, api_version=None, base_url=None, test=False, timeout=None):

        if base_url and api_version:
            raise TranscoderError('Cannot set both `base_url` and `api_version`.')

        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://transcoder.discoverstuff.com/api/'

            if not api_version:
                api_version = 'v1'

            self.base_url = '{0}{1}/'.format(self.base_url, api_version)

        self.api_key = api_key

        self.test = test

        args = (self.base_url, self.api_key)

        kwargs = {
            'api_version': api_version,
            'test': self.test,
            'timeout': timeout
        }

        self.job = Job(*args, **kwargs)
        self.output = Output(*args, **kwargs)
        self.input = Input(*args, **kwargs)
        self.report = None


class Response(object):
    def __init__(self, code, body, raw_body, raw_response):
        self.code = code
        self.body = body
        self.raw_body = raw_body
        self.raw_response = raw_response


class Output(HTTPBackend):
    def __init__(self, *args, **kwargs):
        kwargs['resource_name'] = 'outputs'
        super(Output, self).__init__(*args, **kwargs)

    def details(self, output_id):
        return self.get(self.base_url + '/%s/' % str(output_id))


class Input(HTTPBackend):
    def __init__(self, *args, **kwargs):
        kwargs['resource_name'] = 'inputs'
        super(Input, self).__init__(*args, **kwargs)

    def details(self, input_id):
        return self.get(self.base_url + '/%s/' % input_id)


class Job(HTTPBackend):

    def __init__(self, *args, **kwargs):
        kwargs['resource_name'] = 'jobs'
        super(Job, self).__init__(*args, **kwargs)


    def create(self, input=None, outputs=None, options=None):
        data = {'input': input, 'test': self.test}
        if outputs:
            data['outputs'] = outputs

        if options:
            data.update(options)

        return self.post(self.base_url, body=json.dumps(data))


    def details(self, job_id):
        return self.get(self.base_url + '%s/' % str(job_id))