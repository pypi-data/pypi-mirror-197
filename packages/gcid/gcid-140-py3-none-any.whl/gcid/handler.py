# This file is placed in the Public Domain.


'handler'


import queue
import threading


from .objects import Object, update
from .command import Command


def __dir__():
    return (
            'Handler',
           )


class Handler(Object):

    errors = []

    def __init__(self):
        Object.__init__(self)
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()

    def clone(self, other):
        update(self.cmds, other.cmds)

    def dispatch(self, evt):
        Command.handle(evt)

    def handle(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if func:
            try:
                func(evt)
            except Exception as ex:
                exc = ex.with_traceback(ex.__traceback__)
                Handler.errors.append(exc)

    def loop(self):
        while not self.stopped.set():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    def register(self, cmd, func):
        setattr(self.cbs, cmd, func)

    def stop(self):
        self.stopped.set()
