# This file is placed in the Public Domain.


"introsprection"


import importlib
import inspect
import os


from .command import Command
from .storage import Storage


def importer(name, path):
    mod = None
    spec = importlib.util.spec_from_file_location(name, path)
    if spec:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    scan(mod)
    return mod


def init(mname, path=None):
    mod = importer(mname, path)
    if "init" in dir(mod):
        mod.init()


def scan(mod):
    scancls(mod)
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd.__name__, cmd)


def scancls(mod):
    for _key, clz in inspect.getmembers(mod, inspect.isclass):
        Storage.add(clz)


def scandir(path, func):
    res = []
    if not os.path.exists(path):
        return res
    for fnm in os.listdir(path):
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        mname = fnm.split(os.sep)[-1][:-3]
        path2 = os.path.join(path, fnm)
        res.append(func(mname, path2))
    return res
