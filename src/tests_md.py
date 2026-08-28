import unittest
from webtest import TestApp
import flaresolverr
from dtos import V1ResponseBase

class TestFlareSolverr(unittest.TestCase):
    app = TestApp(flaresolverr.app)
    # wait until the server is ready
    app.get('/')

    def test_v1_endpoint_request_get_cloudflare(self):
        sites_get = [
            ('mardraze', 'https://mardraze.pl', 'Mardraze Software')
        ]
        for site_name, site_url, site_text in sites_get:
            with self.subTest(msg=site_name):
                res = self.app.post_json('/v1', {
                    "cmd": "request.get",
                    "url": site_url,
                    "execJs": "var cb = arguments[0]; setTimeout(function(){ cb(document.title); }, 2000);",
                    "execJsAsync": 1
                })
                body = V1ResponseBase(res.json)
                self.assertIn(site_text, body.solution.jsResult)
                res = self.app.post_json('/v1', {
                    "cmd": "request.get",
                    "url": site_url,
                    "execJs": "return document.title;"
                })
                body = V1ResponseBase(res.json)
                print(body.solution.jsResult)
                self.assertIn(site_text, body.solution.jsResult)

if __name__ == '__main__':
    unittest.main()

