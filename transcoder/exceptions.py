
class TranscoderError(Exception):
    pass


class TranscoderResponseError(Exception):
    def __init__(self, http_response, content):
        self.http_response = http_response
        self.content = content
