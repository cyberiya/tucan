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

from downloader import Downloader
from uploader import Uploader

class Plugin(object):
	""""""
	def __init__(self):
		""""""
		self.active_downloads = {}
		self.active_uploads = {}

	def _download(self, url, wait=None, cookie=None):
		""""""
		if not url in self.active_downloads:
			th = Downloader(url, wait, cookie)
			th.start()
			self.active_downloads[url] = th
	
	def _upload(self, file_name, wait=None, cookie=None):
		""""""
		if not url in self.active_uploads:
			th = Uploader(file_name, wait, cookie)
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

	def _get_status(self, url):
		""""""
		result = None
		if url in self.active_downloads:
			result = self.active_downloads[url].status
		elif url in self.active_uploads:
			result = self.active_uploads[url].status
		return result

	def test_link(self, url):
		"""Metodo virtual que debe ser implementado por cada plugin final."""
		pass

if __name__ == "__main__":
    p = Plugin()