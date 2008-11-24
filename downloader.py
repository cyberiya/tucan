###############################################################################
##	Tucan Project

##	Copyright (C) 2008 Fran Lupion Crakotak(at)yahoo.es
##	Copyright (C) 2008 Paco Salido beakman(at)riseup.net
##	Copyright (C) 2008 JM Cordero betic0(at)gmail.com

##	This program is free software; you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation; either version 2 of the License, or
##	(at your option) any later version.

##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.

##	You should have received a copy of the GNU General Public License
##	along with this program; if not, write to the Free Software
##	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import urllib2
import threading
import time

import cons

BUFFER_SIZE = 2048

class Downloader(threading.Thread):
	""""""
	def __init__(self, url, file_name, wait=None, cookie=None):
		""""""
		threading.Thread.__init__(self)
		self.url = url
		self.file = file_name
		self.wait = wait		
		self.stop_flag = False
		self.start_time = time.time()
		self.elapsed_time = 0
		self.total_size = 0
		self.actual_size = 0
		self.status = cons.STATUS_STOP
		
	def run(self):
		""""""
		if self.wait:
			self.status = cons.STATUS_WAIT
			while self.wait > 0:
				time.sleep(1)
				self.wait -= 1
				self.elapsed_time = self.wait
		f = open(self.file, "w")
		handle = urllib2.urlopen(urllib2.Request(self.url))
		self.total_size = int(handle.info().getheader("Content-Length"))
		self.status = cons.STATUS_ACTIVE
		actual_time = time.time()
		data = handle.read(BUFFER_SIZE)
		f.write(data)
		self.elapsed_time = time.time() - actual_time
		self.actual_size += len(data)
		while ((len(data) > 0) and not self.stop_flag):
			actual_time = time.time()
			data = handle.read(BUFFER_SIZE)
			f.write(data)
			self.actual_size += len(data)
			self.elapsed_time = time.time() - actual_time
		self.stop_flag = True
		self.elapsed_time = time.time() - self.start_time
		if self.actual_size == self.total_size:
			self.status = cons.STATUS_CORRECT
		else:
			self.status = cons.STATUS_INCORRECT