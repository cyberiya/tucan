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
import __builtin__
import unittest

import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "../../"))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "../../default_plugins/"))

from core.events import Events
import core.cons as cons

from megaupload.anonymous_download import AnonymousDownload

TEST_DIR = "/tmp/"
TEST_LINK = "http://www.megaupload.com/?d=3VCUBE3Y"
TEST_NAME = "prueba.bin"
TEST_SIZE = 113
TEST_UNIT = "KB"

class TestAnonymous(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		__builtin__.events = Events()
		self.plugin = AnonymousDownload("mierda", "")

	def test_check_link(self):
		""""""
		name, size, unit = self.plugin.check_links(TEST_LINK)
		self.assertEqual(name, TEST_NAME, "%s != %s" % (name, TEST_NAME))
		self.assertEqual(size, TEST_SIZE, "%s != %i" % (size, TEST_SIZE))
		self.assertEqual(unit, TEST_UNIT, "%s != %s" % (unit, TEST_UNIT))

	def test_download(self):
		""""""
		self.assertTrue(self.plugin.add(TEST_DIR, TEST_LINK, TEST_NAME), "check slots or limits")
		status = cons.STATUS_WAIT
		while ((status != cons.STATUS_ERROR) and (status != cons.STATUS_CORRECT)):
			status, progress, actual_size, unit, speed, time_ = self.plugin.get_status(TEST_NAME)
			time.sleep(1)
		name = "%s%s" % (TEST_DIR, TEST_NAME)
		self.assertTrue(os.path.exists(name), "Not Found: %s" % name)
		f1 = file(TEST_NAME, "r")
		f2 = file(name, "r")
		local = f1.read()
		remote = f2.read()
		f1.close()
		f2.close()
		os.remove(name)
		self.assertEqual(local, remote, "%i != %i" % (len(local), len(remote)))

	def tearDown(self):
		""""""
		del self.plugin

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.ERROR)
	unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestAnonymous))

