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

from base_tests import TestBaseDownload

from megaupload.anonymous_download import AnonymousDownload

TEST_INVALID_LINK = "http://www.megaupload.com/?d=0"
TEST_LINK = "http://www.megaupload.com/?d=3VCUBE3Y"
TEST_SIZE = 113
TEST_UNIT = "KB"

class TestAnonymous(TestBaseDownload):
	""""""
	def setUp(self):
		""""""
		self.plugin = AnonymousDownload("mierda", "")
		self.invalid_link = TEST_INVALID_LINK
		self.link = TEST_LINK
		self.size = TEST_SIZE
		self.unit = TEST_UNIT

	def tearDown(self):
		""""""
		del self.plugin

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.ERROR)

	import __builtin__
	from core.events import Events
	__builtin__.events = Events()
	
	import unittest
	unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestAnonymous))
