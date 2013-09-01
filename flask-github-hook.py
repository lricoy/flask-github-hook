import json
import os
import commands
import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def home():
        payload = json.loads(request.form['payload'])
        branch = os.path.basename(payload['ref'])
        app.logger.debug('Affected branch: {0}'.format(branch))

        pr = subprocess.Popen("/usr/bin/git pull origin {0}".format(branch),
                 cwd = os.path.dirname('/var/www/landpage/' ),
                 shell = True,
                 stdout = subprocess.PIPE,
                 stderr = subprocess.PIPE
        )
        (out, error) = pr.communicate()

        print "Error : " + str(error)
        print "out : " + str(out)

        return 'Thanks for all the fish.'

if __name__ == "__main__":
        app.run()
