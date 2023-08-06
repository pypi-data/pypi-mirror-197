#!/usr/bin/env python3
# This file is placed in the Public Domain.


'console utilities'


import atexit
import getpass
import os
import pwd
import readline
import rlcompleter
import sys
import termios
import traceback


from .clients import Client
from .handler import Handler
from .message import Message


class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        sys.stdout.write(txt)
        sys.stdout.write("\n")
        sys.stdout.flush()


class Console(CLI):

    def handle(self, event):
        CLI.handle(self, event)

    def poll(self):
        event = Message()
        event.orig = repr(self)
        event.txt = input('> ')
        event.parse(event.txt)
        return event


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        super().__init__()
        self.matches = []
        self.options = options

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None


def setcompleter(optionlist):
    completer = Completer(optionlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open('/dev/null', 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    sos = open('/dev/null', 'a+')
    ses = open('/dev/null', 'a+')
    os.dup2(sos.fileno(), sys.stdout.fileno())
    os.dup2(ses.fileno(), sys.stderr.fileno())


def privileges(username):
    if os.getuid() != 0:
        return
    try:
        pwnam = pwd.getpwnam(username)
    except KeyError:
        username = getpass.getuser()
        pwnam = pwd.getpwnam(username)
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def waiter():
    got = []
    for ex in Handler.errors:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        got.append(ex)
    for exc in got:
        Handler.errors.remove(exc)


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)
