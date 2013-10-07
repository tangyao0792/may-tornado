from sys import stderr
from select import epoll
import select
import utils
import os
import time

_EPOLLIN = select.EPOLLIN
PIPE_NAME = '/tmp/mt_waker_pipe'

def make_waker():
    '''Wake the polling loop, to stop the process.'''
    global PIPE_NAME
    if os.path.exists(PIPE_NAME):
        os.system('rm %s' % PIPE_NAME)
    os.mkfifo(PIPE_NAME)
    return os.open(PIPE_NAME, os.O_NONBLOCK | os.O_RDONLY)

class IOLoop:
    def __init__(self):
        self._impl = epoll()
        self._waker = make_waker()
        self._impl.register(self._waker, _EPOLLIN)
        self._handlers = dict()

    @staticmethod
    def Instance():
        '''Singleton pattern. Return a global ioloop instance.'''
        if not hasattr(IOLoop, '_instance'):
            IOLoop._instance = IOLoop()
        return IOLoop._instance

    def add_handler(self, fd, handler, events):
        self._handlers[fd] = handler
        self._impl.register(fd, events)

    def start(self):
        '''The main poll loop. When a event happen, call the handler to handle.'''
        global PIPE_NAME
        while True:
            event_pairs = self._impl.poll(-1)
            try:
                for fd, event in event_pairs:
                    if fd == self._waker:
                        utils.log('Stop.')
                        os.unlink(PIPE_NAME)
                        return
                    self._handlers[fd](fd, event)
                    utils.log('fd: %s, event: %s, handler: %s' % (fd, event, self._handlers[fd]))
            except Exception as e:
                utils.log(str(e), utils.ERROR)
