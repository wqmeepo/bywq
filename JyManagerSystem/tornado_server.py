from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from manage import app
from tornado.ioloop import IOLoop

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000, "0.0.0.0")  # 监听5000端口，作为服务器这里配置成0.0.0.0，服务器就可以监听所有浏览器的访问了。
IOLoop.instance().start()
