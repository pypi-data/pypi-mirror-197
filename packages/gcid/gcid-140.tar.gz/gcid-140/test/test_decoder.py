# This file is placed in the Public Domain.


import unittest


from gcid.decoder import loads
from gcid.encoder import dumps
from gcid.objects import Object


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = 'bla'
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, 'bla')

