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
		self.__name__ = None
		self.__version__ = None
		self.__author__ = None
		self.active_downloads = {}
		self.active_uploads = {}
		self.stoped_downloads = {}
		self.stoped_uploads = {}

	def _download(self, url, wait=None, cookie=None):
		""""""
		if not url in self.active_downloads:
			th = Downloader(url, self._stop_download, wait, cookie)
			th.start()
			self.active_downloads[url] = th
	
	def _upload(self, file_name, wait=None, cookie=None):
		""""""
		if not file_name in self.active_uploads:
			th = Uploader(file_name, self._stop_upload, wait, cookie)
			th.start()
			self.active_uploads[file_name] = th
	
	def _stop_download(self, url):
		""""""
		if url in self.active_downloads:
			self.active_downloads[url].stop_flag = True
			self.stoped_downloads[url] = self.active_downloads[url]
			del self.active_downloads[url]
	
	def _stop_upload(self, file_name):
		""""""
		if file_name in self.active_uploads:
			self.active_uploads[file_name].stop_flag = True
			self.stoped_uploads[file_name] = self.active_uploads[file_name]
			del self.active_uploads[file_name]

	def get_status(self, url):
		""""""
		result = None
		if url in self.active_downloads:
			result = self.active_downloads[url].status
		elif url in self.active_uploads:
			result = self.active_uploads[url].status
		elif url in self.stoped_downloads:
			result = self.stoped_downloads[url].status
			del self.stoped_downloads[url]
		elif url in self.stoped_uploads:
			result = self.stoped_uploads[url].status
			del self.stoped_uploads[url]
		return result

	def test_link(self, url):
		"""Metodo virtual que debe ser implementado por cada plugin final."""
		pass
	
	def get_info(self):
		""""""
		return self.__name__, self.__version__, self.__author__