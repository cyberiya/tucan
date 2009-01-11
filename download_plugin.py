###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion Crakotak(at)yahoo.es
## Copyright (C) 2008-2009 Paco Salido beakman(at)riseup.net
## Copyright (C) 2008-2009 JM Cordero betic0(at)gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
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

from downloader import Downloader

import cons

class DownloadPlugin(object):
	""""""
	def __init__(self):
		""""""
		self.active_downloads = {}

	def start(self, path, url, file_name, wait=None, cookie=None, form=None):
		""""""
		if file_name not in self.active_downloads:
			th = Downloader(path, url, file_name, wait, cookie, form)
			th.start()
			self.active_downloads[file_name] = th
			return True
	
	def stop(self, file_name):
		""""""
		if file_name in self.active_downloads:
			self.active_downloads[file_name].stop_flag = True
			self.active_downloads[file_name].status = cons.STATUS_STOP
			return True
	
	def get_status(self, file_name):
		"""return (status, progress, actual_size, unit, speed, time)"""
		result = None, None, None, None, None, None
		th = None
		if file_name in self.active_downloads:
			th = self.active_downloads[file_name]
			if self.active_downloads[file_name].stop_flag:
				del self.active_downloads[file_name]
		if th:
			actual_size, unit = self.get_size(th.actual_size)
			if th.status == cons.STATUS_ACTIVE:
				progress = int((float(th.actual_size)/float(th.total_size))*100)
				speed = th.get_speed()
				if speed > 0:
					time = int(float((th.total_size - th.actual_size)/1024)/float(speed))
				else:
					time = 0
			else:
				progress = 0
				speed = 0
				time = int(th.time_remaining)
			result = th.status, progress, actual_size, unit, speed, time
		return result

	def check_link(self, url):
		"""Metodo virtual que debe ser implementado por cada plugin final."""
		pass
	
	def get_size(self, num):
		""""""
		result = 0, cons.UNIT_KB
		tmp = int(num/1024)
		if  tmp > 0:
			result = tmp, cons.UNIT_KB
			tmp = int(tmp/1024)
			if tmp > 0:
				result = tmp, cons.UNIT_MB
		return result