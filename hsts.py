import tornado.httpserver
import tornado.ioloop
import tornado.web

class HSTSCookie(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        if self.request.protocol == 'https':
            self.set_header('Strict-Transport-Security', 'max-age=31536000')
        self.write(self.request.protocol)
        self.write('<br>')
        self.write(self.request.host)


class Home(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write('<html><head><script src="hsts.js"></script></head><body></body></html>')


class HSTSScript(tornado.web.RequestHandler):
    def get(self):
        with open('hsts.js', 'r') as f:
            script = f.read()
            script = script.replace('[HOSTNAME]', 'o.marketing-cloud.io')
            self.write(script)

application = tornado.web.Application([
    (r'/', Home),
    (r'/h.gif', HSTSCookie),
    (r'/hsts.js', HSTSScript),
])

if __name__ == '__main__':
    https_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": "/etc/letsencrypt/live/o.marketing-cloud.io/cert.pem",
        "keyfile": "/etc/letsencrypt/live/o.marketing-cloud.io/privkey.pem",
    })
    http_server = tornado.httpserver.HTTPServer(application)
    https_server.listen(443)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
