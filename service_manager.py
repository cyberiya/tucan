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

import urlparse
import re

import cons

from download_manager import DownloadManager

from plugin import Plugin
from plugins import *

class ServiceManager:
	""""""
	def __init__(self):
		""""""
		self.download_manager = DownloadManager(self.get_plugin)
		self.services = []
		self.anonymous_plugins = {}
		self.user_plugins = {}
		self.premium_plugins = {}
		for plugin in Plugin.__subclasses__():
			if plugin.__name__ == cons.TYPE_ANONYMOUS:
				self.init_plugin(plugin, self.anonymous_plugins)
			elif plugin.__name__ == cons.TYPE_USER:
				self.init_plugin(plugin, self.user_plugins)
			elif plugin.__name__ == cons.TYPE_PREMIUM:
				self.init_plugin(plugin, self.premium_plugins)

	def init_plugin(self, plugin_type, dict):
		""""""
		for plugin in plugin_type.__subclasses__():
			dict[plugin.__name__] = plugin()
			if not dict[plugin.__name__].service in self.services:
				self.services.append(dict[plugin.__name__].service)
		
	def get_plugin(self, service, name=None):
		""""""
		result = None, None
		if name:
			if name in self.anonymous_plugins:
				result = name, self.anonymous_plugins[name]
			elif name in self.user_plugins:
				result = name, self.user_plugins[name]
			elif name in self.premium_plugins:
				result = name, self.premium_plugins[name]
		elif service in self.services:
			for plugin_name, plugin in self.anonymous_plugins.items():
				if plugin.service == service:
					result = plugin_name, plugin
			for plugin_name, plugin in self.user_plugins.items():
				if plugin.service == service:
					result = plugin_name, plugin
			for plugin_name, plugin in self.premium_plugins.items():
				if plugin.service == service:
					result = plugin_name, plugin
		return result
					
	def filter_service(self, links):
		""""""
		services = {cons.TYPE_UNSUPPORTED: []}
		for link in links:
			found = False
			print link
			if urlparse.urlparse(link).scheme == "http":
				link = "http" + link.split("http").pop()
				for service in self.services:
					if link.find(service) > 0:
						found = True
						if service in services:
							services[service].append(link)
						else:
							services[service] = [link]
				if not found:
						services[cons.TYPE_UNSUPPORTED].append(link)
		return services
		
	def link_check(self, link, service):
		"""return (active, file_name, int_size, size_unit, plugin)"""
		plugin_name, plugin = self.get_plugin(service)
		name, size, unit = plugin.check_link(link)
		if unit == cons.UNIT_KB:
			tmp_size = int(size/1024)
			if tmp_size > 0:
				size = tmp_size
				unit = cons.UNIT_MB
		return name, size, unit, plugin_name

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
		return packages

	def stop_all(self):
		""""""
		self.download_manager.quit()
	
	def prueba(self):
		""""""
		import time
		plugin = self.anonymous_plugins["AnonymousMegaupload"]
		link = "http://www.megaupload.com/?d=QNVY9GXH"
		name, size, size_unit = plugin.check_link(link)
		print plugin.add_download("/home/crak/downloads/", link, name)
		while len(plugin.active_downloads) > 0:
			print plugin.get_status(name)
			time.sleep(5)

if __name__ == "__main__":
	s = ServiceManager()
	#s.prueba()