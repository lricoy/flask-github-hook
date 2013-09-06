class GitCommandErrorException(Exception):
    def __init__(self, out, error, *args, **kwargs):
        self.out = out
        self.error = error
        super(GitCommandErrorException, self).__init__(*args, **kwargs)

class RepoDoesNotExists(Exception):
    def __init__(self, repo, *args, **kwargs):
        self.repo = repo
        super(RepoDoesNotExists, self).__init__(*args, **kwargs)

class MissingPayloadParam(Exception):
    pass

class InvalidPayloadParam(Exception):
    pass