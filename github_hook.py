import json
import os
import subprocess

from flask import Flask, request
from settings import *

app = Flask(__name__)
app.debug = DEBUG

@app.route('/<repository>', methods=['POST'])
def home(repository):

    # Check the existence of the github payload param
    form_data = request.form.get('payload', '')
    if not form_data:
        return 'Missing payload data.', 403

    # Get the request data.
    payload = json.loads(form_data)
    remote = request.args.get('remote', 'origin')
    branch = os.path.basename(payload['ref'])

    # Local repository path.
    repo_path = os.path.join(REPO_ROOT_PATH, repository)

    # Check the existence of the repository on the server.
    if not os.path.exists(repo_path):
        return 'The given repository name ({repo}) does not exists on the server'.format(repo=repository)

    app.logger.debug('Affected branch: {0} on repo {1}'.format(branch, repository))

    # Build the 'git pull' request.
    exec_command = '{git_exec_path}git pull origin {branch}'.format(git_exec_path=GIT_EXEC_PATH, branch=branch)
    app.logger.debug(exec_command)

    # System call.
    pr = subprocess.Popen(exec_command,
       cwd = repo_path,
       shell = True,
       stdout = subprocess.PIPE,
       stderr = subprocess.PIPE
       )
    (out, error) = pr.communicate()

    app.logger.info("Out : " + str(error))
    app.logger.info("Out : " + str(out))

    # Check the result
    if not 'Error' in error or 'fatal' in error:
        return'So long and thanks for all the fish.'

    else:
        return 'Something went wrong\n {stack}'.format(stack=error), 500

if __name__ == "__main__":
    app.run()
