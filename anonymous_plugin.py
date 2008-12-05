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

from plugin import Plugin

class AnonymousPlugin(Plugin):
	""""""
	def __init__(self, downloads, uploads):
		""""""
		Plugin.__init__(self)
		self.max_downloads = downloads
		self.max_uploads = uploads
		self.download_slots = downloads
		self.upload_slots = uploads
		
	def download(self, path, url, file_name, wait):
		""""""""
		if self.download_slots > 0:
			if self._download(path, url, file_name, wait):
				self.download_slots -= 1
				return True

	def upload(self, file_name):
		""""""""
		if self.upload_slots > 0:
			if self._upload(file_name):
				self.upload_slots -= 1
				return True
				
	def stop_download(self, file_name):
		""""""
		if self.download_slots <= self.max_downloads:
			if self._stop_download(file_name):
				self.download_slots += 1
				return True
		
	def stop_upload(self, file_name):
		""""""
		if self.upload_slots <= self.max_uploads:
			if self._stop_upload(file_name):
				self.upload_slots += 1
				return True
				
	def download_avaible(self):
		""""""
		if self.download_slots > 0:
			return True
			
	def return_download_slot(self):
		""""""
		if self.download_slots <= self.max_downloads:
			self.download_slots += 1
			return True
