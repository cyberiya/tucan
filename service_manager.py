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
		self.anonymous_plugins = {}
		self.user_plugins = {}
		self.premium_plugins = {}
		for plugin in Plugin.__subclasses__():
			if plugin.__name__ == "AnonymousPlugin":
				for plugin in plugin.__subclasses__():
					self.anonymous_plugins[plugin.__name__]= plugin()
			elif plugin.__name__ == "UserPlugin":
				for plugin in plugin.__subclasses__():
					self.user_plugins[plugin.__name__]= plugin()
			elif plugin.__name__ == "PremiumPlugin":
				for plugin in plugin.__subclasses__():
					self.premium_plugins[plugin.__name__]= plugin()
	
	def prueba(self, url):
		""""""
		plugin = self.anonymous_plugins["AnonymousRapidshare"]
		plugin.add_download(url)
		plugin.wait(1)
		print plugin.active_downloads
		plugin.stop_download(url)
		print plugin.active_downloads

if __name__ == "__main__":
    s = ServiceManager()
    s.prueba("cojones")