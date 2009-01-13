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

import threading

import cons

MAX_DOWNLOADS = 3

class Link:
	""""""
	def __init__(self, url, plugin):
		""""""
		self.active = False
		self.url = url
		self.plugin = plugin

class DownloadItem:
	""""""
	def __init__(self, path, name, links, total_size, size_unit):
		""""""
		self.path = path
		self.name = name
		self.status = cons.STATUS_PEND
		self.links = []
		for url, plugin in links:
			self.links.append(Link(url, plugin))
		self.progress = 0
		self.total_size = total_size
		self.actual_size = 0
		self.size_unit = size_unit
		self.speed = 0
		self.time = 0
		
	def update(self, status=cons.STATUS_STOP, progress=0, actual_size=0, size_unit=None, speed=0, time=0):
		""""""
		self.status = status
		self.progress = progress
		self.actual_size = actual_size
		self.size_unit = size_unit
		self.speed = speed
		self.time = time

class DownloadManager:
	""""""
	def __init__(self, max):
		""""""
		self.max_downloads = max
		self.pending_downloads = []
		self.active_downloads = []
		self.complete_downloads = []
		self.timer = None
		self.scheduling = False
		
	def delete_link(self, name, link):
		""""""
		for download in self.pending_downloads:
			if download.name == name:
				for url in download.links:
					if link == url.url:
						del download.links[download.links.index(url)]
						return True
		
	def get_files(self):
		""""""
		result = []
		for downloads in [self.pending_downloads, self.active_downloads, self.complete_downloads]:
			for download in downloads:
				result.append(download)
		self.update()
		return result
		
	def clear(self, files):
		""""""
		for name in files:
			complete = [tmp.name for tmp in self.complete_downloads]
			if name in complete:
				print "Cleared ", name
				del self.complete_downloads[complete.index(name)]

	def add(self, path, name, links, total_size, size_unit):
		""""""
		if ((name not in [tmp.name for tmp in self.active_downloads]) and (not name in [tmp.name for tmp in self.pending_downloads])):
			self.pending_downloads.append(DownloadItem(path, name, links, total_size, size_unit))
			threading.Timer(1, self.scheduler).start()
			self.scheduler
			return True
	
	def start(self, name):
		""""""
		for download in self.pending_downloads:
			if name == download.name:
				for link in download.links:
					print name
					if link.plugin.add(download.path, link.url, download.name):
						link.active = True
						self.active_downloads.append(download)
						self.pending_downloads.remove(download)
						return True
					else:
						download.status = cons.STATUS_PEND
					
	def stop(self, name):
		""""""
		for download in self.pending_downloads:
			if name == download.name:
				download.status = cons.STATUS_STOP
		for download in self.active_downloads:
			if name == download.name:
				for link in download.links:
					if link.active:
						if link.plugin.stop(download.name):
							link.active = False
							download.update()
							self.pending_downloads.append(download)
							self.active_downloads.remove(download)
							return True
	
	def update(self):
		""""""
		for download in self.active_downloads:
			for link in download.links:
				if link.active:
					plugin = link.plugin
			if plugin:
				status, progress, actual_size, unit, speed, time = plugin.get_status(download.name)
				print download.name, status, progress, actual_size, unit, speed, time
				if status:
					download.update(status, progress, actual_size, unit, speed, time)
					if status in [cons.STATUS_PEND, cons.STATUS_STOP, cons.STATUS_ERROR]:
						if status == cons.STATUS_PEND:
							link.plugin.add_wait()
						self.stop(download.name)
					elif status == cons.STATUS_CORRECT:
						download.progress = 100
						link.plugin.return_slot()
						self.complete_downloads.append(download)
						self.active_downloads.remove(download)

	def scheduler(self):
		""""""
		if not self.scheduling:
			print "scheduling"
			self.scheduling = True
			if len(self.pending_downloads) > 0:
				if len(self.active_downloads) < self.max_downloads:
					for download in self.pending_downloads:
						if download.status not in [cons.STATUS_STOP, cons.STATUS_ERROR]:
							print self.start(download.name)
			if self.timer:
				self.timer.cancel()
			self.timer = threading.Timer(15, self.scheduler)
			self.timer.start()
			self.scheduling = False
	
	def quit(self):
		""""""
		if self.timer:
			self.scheduling = True
			self.timer.cancel()
		for download in self.active_downloads:
			for link in download.links:
				link.plugin.stop_all()
