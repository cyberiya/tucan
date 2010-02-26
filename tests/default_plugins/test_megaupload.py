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

import __builtin__
import unittest

import sys
sys.path.append("/home/crak/tucan/0.3.10/")
sys.path.append("/home/crak/tucan/0.3.10/default_plugins/")

from core.events import Events
import core.url_open

from megaupload.anonymous_download import AnonymousDownload

TEST_LINK = "http://www.megaupload.com/?d=3VCUBE3Y"
CHECK_LINK_RESULT = ('prueba.bin', 113, 'KB')

class TestAnonymous(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		__builtin__.events = Events()
		self.plugin = AnonymousDownload("mierda", "")

	def test_check_link(self):
		""""""
		name, size, unit = self.plugin.check_links(TEST_LINK)
		self.assertEqual(name, CHECK_LINK_RESULT[0], "%s != %s" % (name, CHECK_LINK_RESULT[0]))
		self.assertEqual(size, CHECK_LINK_RESULT[1], "%s != %i" % (size, CHECK_LINK_RESULT[1]))
		self.assertEqual(unit, CHECK_LINK_RESULT[2], "%s != %s" % (unit, CHECK_LINK_RESULT[2]))

	def test_download(self):
		""""""
		pass

	def tearDown(self):
		""""""
		pass

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.CRITICAL)
	unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestAnonymous))

