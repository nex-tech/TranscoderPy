from __future__ import absolute_import
from .http import HTTPBackend
from .exceptions import TranscoderError
try:
    import json
except ImportError:
    import simplejson
    json = simplejson


class Transcoder(object):
    def __init__(self, api_username, api_key, api_version=None, base_url=None, test=False, timeout=None):

        if base_url and api_version:
            raise TranscoderError('Cannot set both `base_url` and `api_version`.')

        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://transcoder.discoverstuff.com/api/'

            if not api_version:
                api_version = 'v1'

            self.base_url = '{0}{1}/'.format(self.base_url, api_version)

        self.api_username = api_username
        self.api_key = api_key

        self.test = test

        args = (self.base_url, api_username, self.api_key)

        kwargs = {
            'api_version': api_version,
            'test': self.test,
            'timeout': timeout
        }

        self.job = Job(*args, **kwargs)
        self.output = Output(*args, **kwargs)
        self.input = Input(*args, **kwargs)
        self.report = None


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