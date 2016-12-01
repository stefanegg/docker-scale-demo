#!/usr/bin/env python

import os, sys, socket, signal
from collections import OrderedDict
import hashlib, uuid
import web, json

# routing
urls = (
    '/', 'webapp_root'
)

# get first line of file
def file_head(filename):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        line = f.readline().replace('\n', '')
        f.close()
        return line
    else:
        return '<unknown>'

# handle system signals
def onterm(signum, frame):
    SIGNALS = dict((getattr(signal, n), n) \
        for n in dir(signal) if n.startswith('SIG') and '_' not in n )
    sys.stdout.write('Received signal %s, terminating...\n' % SIGNALS[signum])
    sys.exit(0)

# request/response handler
def set_headers(handle):
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')
    web.header('Access-Control-Allow-Credentials', 'true')
    return handle()

# path /
class webapp_root:
    def GET(self):
        random = hashlib.sha512(uuid.uuid1().hex).hexdigest()
        response = OrderedDict([
            ('container', container),
            ('host', host),
            ('app_version', app_version),
            ('random', random)
            ])
        return json.dumps(response)

# get hostname and container name
container = file_head('/etc/hostname')
host = file_head('/host_hostname')
if container == '<unknown>':
    container = socket.gethostname()

# get app version from environment variable
if 'app_version' in os.environ:
    app_version = os.environ['app_version']
else:
    app_version = '<unknown>'

def main():
    app = web.application(urls, globals())
    app.add_processor(set_headers)
    app.run()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, onterm)
    main()
