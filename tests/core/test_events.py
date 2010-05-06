###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import time
import os.path
import unittest

import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "../../"))

from core.events import *

TEST_1 = "test-1"
ARG_1 = "arg-1"

class TestEvents(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.events = Events()
		
	def callback(self, connect_arg, trigger_arg):
		""""""
		self.assertEqual(connect_arg, trigger_arg, "%s != %s" % (connect_arg, trigger_arg))

	def test_disconnect(self):
		""""""
		id = self.events.connect(TEST_1, self.callback, ARG_1)
		id2 = self.events.connect(TEST_1, self.callback, ARG_1)
		self.events.trigger(TEST_1, ARG_1)
		self.events.trigger(TEST_1, ARG_1)
		self.assertTrue(self.events.disconnect(TEST_1, id), "")
		self.events.trigger(TEST_1, ARG_1)
		self.assertFalse(self.events.disconnect(TEST_1, id), "")
		self.assertTrue(self.events.disconnect(TEST_1, id2), "")

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.ERROR)

	unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestEvents))
