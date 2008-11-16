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
			if plugin.__name__ == "AnonymousPlugin":
				self.init_plugin(plugin, self.anonymous_plugins)
			elif plugin.__name__ == "UserPlugin":
				self.init_plugin(plugin, self.user_plugins)
			elif plugin.__name__ == "PremiumPlugin":
				self.init_plugin(plugin, self.premium_plugins)

	def init_plugin(self, plugin_type, dict):
		""""""
		for plugin in plugin_type.__subclasses__():
			dict[plugin.__name__] = plugin()
			if not dict[plugin.__name__].service in self.services:
				self.services.append(dict[plugin.__name__].service)
	
	def supported_service(self, link):
		""""""
		result = None
		for service in self.services:
			if link.find(service) > 0:
				result = service
		return result

	def filter_service(self, links):
		""""""
		services = {"unsupported": []}
		links = [link.strip() for link in links]
		for link in links:
			service = self.supported_service(link)
			if service:
				if service in services:
					services[service].append(link)
				else:
					services[service] = [link]
			else:
				services["unsupported"].append(link)
		return services
			
	
	def prueba(self, url):
		""""""
		import time
		plugin = self.anonymous_plugins["AnonymousRapidshare"]
		print plugin.add_download(url)
		print plugin.add_download("cojones")
		print plugin.get_status(url)
		time.sleep(3)
		print plugin.get_status(url)
		plugin.stop_download(url)
		print plugin.stoped_downloads
		time.sleep(1)
		print plugin.get_status(url)
		print plugin.stoped_downloads

if __name__ == "__main__":
	s = ServiceManager()
	#s.prueba("mierda")
	f = open("links_example.txt", "r")
	print s.filter_service(f.readlines())
	f.close()
