from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python import log
from man2html import man_process
from subprocess import Popen, PIPE
import string
import os
import os.path
import json


class WebMan(resource.Resource):    
    def render_POST(self, request):
        form = json.load(request.content)

        if 'section' in form:
            section = int(form['section'])
        else:
            section = 0

        if 'apropos' in form and form['apropos'] == '1':
            command = ['apropos']
            if section != 0:
                command.extend(['-s', str(section)])
        else:
            command = ['man', '-P', 'cat']
            if section != 0:
                command.extend(['-S', str(section)])

        # TODO error handling
        query = ''
        manhtml = ''
        if 'query' in form:
            query = form['query']
            if len(query) > 0:
                command.append(query)
                p = Popen(command, stdout=PIPE, stderr=PIPE)
                manhtml = man_process(p.stdout.read().decode('utf8') + p.stderr.read().decode('utf8'))
            else:
                manhtml = 'Empty input. Please type a manual page and search again.'

        request.setHeader("content-type", "application/json")
        # you should not do like this
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST')
        request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
        request.setHeader('Access-Control-Max-Age', '2520') # 48h
        resp = {
            'code': 'success',
            'content': manhtml
        }
        resp = json.dumps(resp).encode('utf-8')
        return resp


class Root(resource.Resource):
    def getChild(self, name, request):
        if name == b'':
            request.redirect(b'man')
            return WebMan()
        return resource.Resource.getChild(self, name, request)


root = Root()
root.putChild(b'man', WebMan())


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from sys import stdout
    log.startLogging(stdout)

    site = server.Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()