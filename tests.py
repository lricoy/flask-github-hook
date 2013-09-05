import os
import json
import unittest

from nose.tools import assert_raises

import github_hook
from util import *

class GitHubHookRequestTestCase(unittest.TestCase):

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

    def test_invalid_payload_param(self):
        resp = self.app.post('/dummy_repo', data={'payload': "{invalid_json '11'}"})
        assert 'Invalid Payload parameter received' in resp.data
        assert resp.status_code == 400

    def test_nonexistent_repository(self):
    	resp = self.app.post('/dummy_repo', data={'payload': json.dumps({"ref": "master"})})
    	assert 'The given repository name (dummy_repo) does not exists on the server' in resp.data
    	assert resp.status_code == 500

    def test_successful_request(self):
        resp = self.app.post(
            os.path.basename(os.path.dirname(__file__)),
            data={'payload' :json.dumps({"ref": "master"})}
        )
        assert resp.data == 'OK'
        assert resp.status_code == 200



class GitUpdaterTestCase(unittest.TestCase):

    def setUp(self):
        self.git = github_hook.GitUpdater('dummy_repo', 'dummy_branch')

    def test_create_dummy_obj(self):
        git = self.git

        assert git.git_exec_path == '/usr/bin/'
        assert git.repository_root_path == '/home/lucas/workspace'
        assert git.repository == 'dummy_repo'
        assert git.branch == 'dummy_branch'

    def test_nonexistant_repo(self):
        assert_raises(RepoDoesNotExists, self.git.update)

    def test_nonexistant_branch(self):
        git = github_hook.GitUpdater(
            os.path.basename(os.path.dirname(__file__))
            , 'dummy_branch'
        )

        assert_raises(GitCommandErrorException, git.update)

if __name__ == '__main__':
    unittest.main()