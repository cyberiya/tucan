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

import threading
import re

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
	def __init__(self, name, links, total_size, size_unit):
		"""links = [(False, url, plugin)]"""
		self.name = name
		self.links = []
		for url, plugin in links:
			self.links.append(Link(url, plugin))
		self.status = cons.STATUS_PEND
		self.progress = 0
		self.total_size = total_size
		self.actual_size = 0
		self.size_unit = size_unit
		self.speed = 0
		self.time = 0
		
	def update(self, status, progress, actual_size, size_unit, speed, time):
		""""""
		self.status = status
		self.progress = progress
		self.actual_size = actual_size
		self.size_unit = size_unit
		self.speed = speed
		self.time = time

class DownloadManager:
	""""""
	def __init__(self, get_plugin):
		""""""
		self.get_plugin = get_plugin
		self.pending_downloads = []
		self.active_downloads = []
		self.complete_downloads = []
		self.timer = None
		self.scheduling = False
		
	def get_files(self):
		""""""
		result = []
		for downloads in [self.active_downloads, self.complete_downloads]:
			for download in downloads:
				result.append(download)
		self.update()
		return result
		
	def create_packages(self, dict):
		""""""
		packages = []
		files = []
		for service, links in dict.items():
			for link in links:
				found = False
				for tmp_link in files:
					if link[1] == tmp_link[1]:
						found = True
						if not service in tmp_link[2]:
							tmp_link[2].append(service)
							tmp_link[0].append(link[0])
							tmp_link[5].append(link[4])
				if not found:
					files.append(([link[0]], link[1], [service], link[2], link[3], [link[4]]))
		while len(files) > 0:
			tmp_name = []
			first = files[0]
			others = files[1:]
			for link in others:
				chars = re.split("[0-9]+", link[1])
				nums = re.split("[^0-9]+", link[1])
				tmp = ""
				for i in chars:
					if tmp+i == first[1][0:len(tmp+i)]:
						tmp += i
						for j in nums:
							if tmp+j == first[1][0:len(tmp+j)]:
								tmp += j
				tmp_name.append(tmp)
			final_name = ""
			for name in tmp_name:
				if len(name) > len(final_name):
					final_name = name
			if len(final_name) > 0:
				packages.append((final_name, [first]))
				del files[files.index(first)]
				tmp_list = []
				for link in files:
					if final_name in link[1]:
						tmp_list.append(link)
				for package_name, package_files in packages:
					if package_name == final_name:
						package_files += tmp_list
				for i in tmp_list:
					del files[files.index(i)]
			else:
				alone_name = first[1]
				alone_name = alone_name.split(".")
				alone_name.pop()
				alone_name = ".".join(alone_name)
				packages.append((alone_name, [first]))
				del files[files.index(first)]
		for package_name, package_downloads in packages:
			for download in package_downloads:
				tmp = []
				for service in download[2]:
					plugin_name, plugin = self.get_plugin(service)
					tmp.append((download[0][download[2].index(service)], plugin))
				self.add(download[1], tmp, download[3], download[4])
		return packages

	def add(self, name, links, total_size, size_unit):
		""""""
		if ((name not in [tmp.name for tmp in self.active_downloads]) and (not name in [tmp.name for tmp in self.pending_downloads])):
			self.pending_downloads.append(DownloadItem(name, links, total_size, size_unit))
			self.scheduler()
			return True
	
	def remove(self, name):
		""""""
		if name in [tmp.name for tmp in self.active_downloads]:
			self.stop(name)
		for download in self.pending_downloads:
			if name == download.name:
				self.pending_downloads.remove(download)
				return True
	
	def start(self, name):
		""""""
		for download in self.pending_downloads:
			if name == download.name:
				for link in download.links:
					if link.plugin.add_download(link.url, download.name):
						link.active = True
						self.active_downloads.append(download)
						self.pending_downloads.remove(download)
						return True
					
	def stop(self, name):
		""""""
		print "stoped"
		for download in self.active_downloads:
			if name == download.name:
				for link in download.links:
					if link.active:
						if link.plugin.stop_download(download.name):
							link.status = cons.STATUS_STOP
							return True
	
	def update(self):
		""""""
		for download in self.active_downloads:
			for link in download.links:
				if link.active:
					plugin = link.plugin
			if plugin:
				status, progress, actual_size, unit, speed, time = plugin.get_status(download.name)
				download.update(status, progress, actual_size, unit, speed, time)
				print status, progress, actual_size, unit, speed, time
				if ((status == cons.STATUS_STOP) or (status == cons.STATUS_ERROR)):
					link.active = False
					link.progress = 0
					self.pending_downloads.append(download)
					self.active_downloads.remove(download)
				elif status == cons.STATUS_CORRECT:
					self.complete_downloads.append(download)
					self.active_downloads.remove(download)

	def scheduler(self):
		""""""
		print "scheduling"
		if not self.scheduling:
			self.scheduling = True
			if len(self.pending_downloads) > 0:
				if len(self.active_downloads) < MAX_DOWNLOADS:
					for download in self.pending_downloads:
						self.start(download.name)
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
			print self.stop(download.name)
