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

SIZE = 10240

class UploadMockup:
	""""""
	def __init__(self, url, get_speed, update):
		""""""
		speed = 1
		actual_size = 0
		while speed and actual_size < SIZE:
			time.sleep(1)
			speed = get_speed()
			actual_size += speed
			if actual_size > SIZE:
				actual_size = SIZE
			update(actual_size, speed)

class TestUploadManager(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		pass
		
	def get_speed(self):
		""""""
		return 4096
		
	def update(self, current_size, actual_speed):
		print current_size
		print actual_speed
		
	def add(self):
		pass
	
	def start(self):
		pass
	
	def stop(self):
		pass

	def clear(self):
		pass
		
	def scheduler(self):
		pass

	def test_upload_mockup(self):
		""""""
		upload = UploadMockup("something", self.get_speed, self.update)

	def tearDown(self):
		""""""
		pass
