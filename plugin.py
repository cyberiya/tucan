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

import cons

class Plugin(object):
	""""""
	def __init__(self):
		""""""
		self.__name__ = None
		self.__version__ = None
		self.__author__ = None
		self.active_downloads = {}
		self.active_uploads = {}

	def _download(self, url, file_name, wait=None, cookie=None):
		""""""
		if not file_name in self.active_downloads:
			th = Downloader(url, file_name, wait, cookie)
			th.start()
			self.active_downloads[file_name] = th
	
	def _upload(self, url, file_name, wait=None, cookie=None):
		""""""
		if not file_name in self.active_uploads:
			th = Uploader(file_name, wait, cookie)
			th.start()
			self.active_uploads[file_name] = th
	
	def _stop_download(self, file_name):
		""""""
		if url in self.active_downloads:
			self.active_downloads[file_name].stop_flag = True
			del self.active_downloads[file_name]
	
	def _stop_upload(self, file_name):
		""""""
		if file_name in self.active_uploads:
			self.active_uploads[file_name].stop_flag = True
			del self.active_uploads[file_name]

	def get_status(self, file_name):
		"""return (status, actual_size, time)"""
		result = None, None, None
		if file_name in self.active_downloads:
			result = self.active_downloads[file_name].status, self.active_downloads[file_name].actual_size, self.active_downloads[file_name].elapsed_time
			if self.active_downloads[file_name].stop_flag:
				del self.active_downloads[file_name]
		elif file_name in self.active_uploads:
			result = self.active_uploads[file_name].status, self.active_uploads[file_name].actual_size, self.active_uploads[file_name].elapsed_time
			if self.active_uploadsloads[file_name].stop_flag:
				del self.active_uploads[file_name]
		return result

	def check_link(self, url):
		"""Metodo virtual que debe ser implementado por cada plugin final."""
		pass
	
	def get_info(self):
		""""""
		return self.__name__, self.__version__, self.__author__
		

if __name__ == "__main__":
	d = Plugin()
	d._download("http://rapidshare.com/files/151319357/D.S03E02.0TV.cHoPPaHoLiK.part6.rar", "D.S03E02.0TV.cHoPPaHoLiK.part6.rar", 1)
	while len(d.active_downloads) > 0:
		print d.get_status("D.S03E02.0TV.cHoPPaHoLiK.part6.rar")
		time.sleep(0.1)