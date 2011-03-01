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
import unittest

from core.queue import Queue
from core.upload_manager import UploadManager

class TestUploadManager(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.manager = UploadManager(Queue())
		self.manager.scheduling = True
		self.manager.add([('/home/user/file.part1.rar', 1024, ['megaupload.anonymous_upload'])])

	def test_start(self):
		link = self.manager.queue.items[2]
		self.manager.start(2, link)
		while self.manager.get_active_threads():
			pass
	
	def test_stop(self):
		link = self.manager.queue.items[2]
		self.manager.start(2, link)
		time.sleep(2)
		self.manager.stop(2, link)
		while self.manager.get_active_threads():
			pass

	def clear(self):
		pass

	def tearDown(self):
		""""""
		self.manager.quit()
		del self.manager
