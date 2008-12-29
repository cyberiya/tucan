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

HEADER = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4"}

BUFFER_SIZE = 4096

class Downloader(threading.Thread):
	""""""
	def __init__(self, path, url, file_name, wait, cookie, handler):
		""""""
		threading.Thread.__init__(self)
		self.get_handler = handler
		self.status = cons.STATUS_PEND
		self.path = path
		self.url = url
		self.file = file_name
		self.wait = wait
		self.stop_flag = False
		self.start_time = time.time()
		self.time_remaining = 0
		self.total_size = 0
		self.actual_size = 0
		self.speed = 0
		self.tmp_time = 0
		self.tmp_size = 0
		if cookie:
			urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)))
		
	def run(self):
		""""""
		if self.wait:
			self.status = cons.STATUS_WAIT
			while ((self.wait > 0) and not self.stop_flag):
				time.sleep(1)
				self.wait -= 1
				self.time_remaining = self.wait
		if not self.stop_flag:
			try:
				if self.get_handler:
					handle = self.get_handler()
				else:
					handle = urllib2.urlopen(urllib2.Request(self.url, None, HEADER))
				f = open(self.path + self.file, "w")
				self.total_size = int(handle.info().getheader("Content-Length"))
				self.start_time = time.time()
				self.status = cons.STATUS_ACTIVE
				data = "None"
				while ((len(data) > 0) and not self.stop_flag):
					data = handle.read(BUFFER_SIZE)
					f.write(data)
					self.actual_size += len(data)
				self.time_remaining = time.time() - self.start_time
				f.close()
				if not self.stop_flag:
					self.stop_flag = True
					if self.actual_size == self.total_size:
						self.status = cons.STATUS_CORRECT
					else:
						self.status = cons.STATUS_ERROR
			except urllib2.HTTPError, e:
				print "[%4d-%02d-%02d %02d:%02d:%02d]" % time.localtime(time.time())[:6], e
				self.stop_flag = True
				self.status = cons.STATUS_PEND

	def get_speed(self):
		"""return int speed KB/s"""
		elapsed_time = time.time() - self.tmp_time
		size = self.actual_size - self.tmp_size
		if size > 0:
			self.speed = int(float(size/1024)/float(elapsed_time))
			self.tmp_time = time.time()
			self.tmp_size = self.actual_size
		return self.speed