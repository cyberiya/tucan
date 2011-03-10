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
import threading
import logging
logger = logging.getLogger(__name__)

import cons

import random

class Uploader(threading.Thread):
	""""""
	def __init__(self, item):
		""""""
		threading.Thread.__init__(self)
		self.item = item
		self.speed = 0
		self.max_speed = 0
		self.stop_flag = False
	
	def limit_speed(self, speed):
		""""""
		self.max_speed = speed

	def upload(self):
		""""""
		time.sleep(random.random()*0.01)
		return 1024*4

	def run(self):
		"""Parsing and Poster work"""
		while not self.stop_flag and self.item.current_size < self.item.total_size:
			remaining_time = 1
			size = 0
			total_time = time.time()
			while remaining_time > 0 and not self.stop_flag:
				start_time = time.time()
				size += self.upload()
				remaining_time -= time.time() - start_time
				if self.max_speed and size >= self.max_speed:
					if remaining_time > 0:
						time.sleep(remaining_time)
					break
			#print time.time() - total_time
			self.item.update(size, size-self.speed)
			self.speed = size
		if self.stop_flag:
			self.item.set_status(cons.STATUS_STOP)
		else:
			self.item.set_status(cons.STATUS_CORRECT)

	def stop(self):
		"""Set a flag so that it stops"""
		self.stop_flag = True
