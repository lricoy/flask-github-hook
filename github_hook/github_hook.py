"""
    Flask Github Hook
    ~~~

    Simple module that integrate github post-receive signal with local git-pull update.

"""

import json
import os
dirname = os.path.dirname
import subprocess

from flask import Flask, request
from util import *

app = Flask(__name__)
app.debug = True

@app.route('/<repository>', methods=['POST'])
def default(repository):
    """Default method that handle the git post-receive request.

    :param repository: The name of the repository to update.
    """

    try:
        payload = ''
        remote = request.args.get('remote', 'origin')

        try:
            form_data = request.form['payload']
            payload = json.loads(form_data)
            branch = os.path.basename(payload['ref'])

        except KeyError, e:
            raise MissingPayloadParam()

        except Exception, e:
            raise InvalidPayloadParam()
        
        git = GitUpdater(repository, branch)
        git.update()

        return 'OK', 200

    except RepoDoesNotExists, e:
        return 'The given repository name ({repo}) does not exists on the server'.format(repo=e.repo), 500

    except MissingPayloadParam, e:
        return 'Missing payload data.', 403

    except InvalidPayloadParam, e:
        return 'Invalid Payload parameter received', 400

    except Exception, e:
        app.logger.error(e)
        return 'Something went wrong\n {stack}'.format(stack=e), 500

class GitUpdater(object):
    """
        Simple class to handle the git commands
    """

    def __init__(self, repo, branch):
        self.git_exec_path = '/usr/bin/'
        self.repository_root_path = dirname(dirname(os.path.abspath(__file__)))
        self.repository = repo
        self.branch = branch

        app.logger.debug('Affected branch: {0} on repo {1} at {2}'.format(branch, repo, self.repository_root_path))

    @property
    def exec_command(self):
        str_command = '{git_exec_path}git pull origin {branch}'.format(**self.__dict__)
        app.logger.debug(str_command)
        return str_command

    def update(self):
        """
            Find the repository local path and execute a 'git pull'
        """
        app.logger.debug(self.__dict__)
        # Local repository path.
        repo_path = os.path.join(self.repository_root_path, self.repository)


        # Check the existence of the repository on the server.
        if not os.path.exists(repo_path):
            raise RepoDoesNotExists(self.repository)

        # System call.
        pr = subprocess.Popen(self.exec_command,
           cwd = repo_path,
           shell = True,
           stdout = subprocess.PIPE,
           stderr = subprocess.PIPE
           )

        (out, error) = pr.communicate()

        app.logger.info("Out : " + str(error))
        app.logger.info("Out : " + str(out))

        # Check the result
        if 'Error' in error or 'fatal' in error:
            raise GitCommandErrorException(out, error)


if __name__ == "__main__":
    app.run()