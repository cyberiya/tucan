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

import cons

from plugin import Plugin
from plugins import *

class ServiceManager:
	""""""
	def __init__(self):
		""""""
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
			size = int(round(size/1024))
			unit = cons.UNIT_MB
		return name, size, unit, plugin_name
	
	def prueba(self):
		""""""
		import time
		plugin = self.premium_plugins["PremiumRapidshare"]
		link = "http://rapidshare.com/files/151319357/D.S03E02.0TV.cHoPPaHoLiK.part6.rar"
		name, size, size_unit = plugin.check_link(link)
		plugin.add_download(link, name)
		while len(plugin.active_downloads) > 0:
			print plugin.get_status(name)
			time.sleep(5)

if __name__ == "__main__":
	s = ServiceManager()
	s.prueba()