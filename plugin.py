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

import time

from downloader import Downloader
from uploader import Uploader

class Plugin(object):
	""""""
	def __init__(self):
		""""""
		self.active_downloads = {}
		self.active_uploads = {}
		
	def add_download(self, url, cookie=None):
		""""""
		if not url in self.active_downloads:
			th = Downloader(url, cookie)
			th.start()
			self.active_downloads[url] = th
	
	def add_upload(self, file_name, cookie=None):
		""""""
		if not url in self.active_uploads:
			th = Uploader(file_name, cookie)
			th.start()
			self.active_uploads[file_name] = th
	
	def stop_download(self, url):
		""""""
		if url in self.active_downloads:
			self.active_downloads[url].stop = True
			del self.active_downloads[url]
	
	def stop_upload(self, file_name):
		""""""
		if url in self.active_uploads:
			self.active_uploads[file_name].stop = True
			del self.active_uploads[file_name]

	def get_status(self, url):
		""""""
		result = None
		if url in self.active_downloads:
			result = self.active_uploads[file_name].status
		elif url in self.active_uploads:
			result = self.active_uploads[file_name].status
		return result

	def get_cookie(self, user, password):
		""""""
		pass

	def wait(self, seconds):
		""""""
		time.sleep(seconds)

	def test_link(self, url):
		"""Metodo virtual que debe ser implementado por cada plugin final."""
		pass

if __name__ == "__main__":
    p = Plugin()