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
		self.download_slots = downloads
		self.upload_slots = uploads
		
	def download(self, url, file_name, wait):
		""""""""
		result = False
		if self.download_slots > 0:
			self.download_slots -= 1
			self._download(url, file_name, wait)
			result = True
		return result

	def upload(self, file):
		""""""""
		result = False
		if self.upload_slots > 0:
			self.upload_slots -= 1
			self._upload(file)
			result = True
		return result
		
	def stop_download(self, link):
		""""""
		self.download_slots += 1
		return self._stop_download(link)
		
	def stop_upload(self, file):
		""""""
		self.upload_slots += 1
		return self._stop_upload(file)
