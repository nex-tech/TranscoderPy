import unittest
from mock import patch

from test_util import TEST_API_KEY, load_response
from transcoder import Transcoder


class TestJobs(unittest.TestCase):

    def setUp(self):
        self.client = Transcoder(api_key=TEST_API_KEY)


    @patch("requests.Session.post")
    def test_job_create(self, post):
        post.return_value = load_response(201, 'fixtures/job_create.json')

        response = self.client.job.create('http://www.ibiblio.org/openvideo/video/umd/anni001.mpg')

        self.assertEquals(response.code, 201)
        self.assertTrue(response.body['id'] > 0)
        self.assertEquals(len(response.body['outputs']), 1)



if __name__ == "__main__":
    unittest.main()
