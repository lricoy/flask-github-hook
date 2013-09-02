import os
import json
import unittest
import github_hook

class GitHubHookTestCase(unittest.TestCase):

    def setUp(self):
        github_hook.app.config['TESTING'] = True
        self.app = github_hook.app.test_client()

    def tearDown(self):
    	pass

    def test_empty_repository_param(self):
        resp = self.app.get('/')
        assert 'Not Found' in resp.data
        assert resp.status_code == 404

    def test_empty_payload_param(self):
    	resp = self.app.post('/dummy_repo')
    	assert 'Missing payload data.' in resp.data
    	assert resp.status_code == 403

    def test_nonexistent_repository(self):
    	resp = self.app.post('/dummy_repo', data={'payload': json.dumps({"ref": "master"})})
    	assert 'The given repository name (dummy_repo) does not exists on the server' in resp.data
    	assert resp.status_code == 500

if __name__ == '__main__':
    unittest.main()