from sys import stderr
from select import epoll
import select

_EPOLLIN = select.EPOLLIN

def log(log_item):
    stderr.write(log_item + '\n')
    stderr.flush()

class IOLoop:
    def __init__(self):
        self._impl = epoll()
        self._handlers = dict()
        pass

    @staticmethod
    def Instance():
        '''
        Singleton pattern. Return a global ioloop instance.
        '''
        if not hasattr(IOLoop, '_instance'):
            IOLoop._instance = IOLoop()
        return IOLoop._instance

    def add_handler(self, fd, handler, events):
        self._handlers[fd] = handler
        self._impl.register(fd, events)

    def start(self):
        while True:
            event_pairs = self._impl.poll(-1)
            try:
                for fd, event in event_pairs:
                    self._handlers[fd](fd, event)
            except Exception as e:
                log(str(e))
