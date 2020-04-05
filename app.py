from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from man2html import man_process
from subprocess import Popen, PIPE
import string
import os
import os.path
import json


class WebMan(resource.Resource):
    def render_GET(self, request):

        if b'section' in request.args:
            section = int(request.args[b'section'][0])
        else:
            section = 0

        if b'apropos' in request.args and request.args[b'apropos'][0] == b'1':
            command = ['apropos']
            if section != 0:
                command.extend(['-s', str(section)])
        else:
            command = ['man', '-P', 'cat']
            if section != 0:
                command.extend(['-S', str(section)])

        # 用 else 语句的话 else 语句也执行了，不懂不懂
        query = ''
        manhtml = ''
        if b'query' in request.args:
            query = str(request.args[b'query'][0], 'utf8')
            if len(query) > 0:
                command.append(query)
                p = Popen(command, stdout=PIPE, stderr=PIPE)
                manhtml = man_process(p.stdout.read().decode('utf8') + p.stderr.read().decode('utf8'))
            else:
                manhtml = 'Empty input. Please type a manual page and search again.'

        request.responseHeaders.addRawHeader(b"content-type", b"application/json")
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

    site = server.Site(root)
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
    endpoint.listen(site)
    reactor.run()