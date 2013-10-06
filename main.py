import ioloop
import httpserver

if __name__ == '__main__':
    http_server = httpserver.HTTPServer(None)
    http_server.listen(8000)
    ioloop.IOLoop.Instance().start()
