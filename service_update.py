###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crakotaku(at)yahoo.es
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

import os
import urllib2

from HTMLParser import HTMLParser

import config
from service_config import ServiceConfig

import cons

BASE = "https://forja.rediris.es/svn/cusl3-tucan/trunk/default_plugins/"
CONF_FILE = "service.conf"

class ServiceList(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.services = []
		self.feed(urllib2.urlopen(urllib2.Request(url)).read())
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "dir":
			self.services.append(attrs[1][1])
			
class ServiceCheck(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.files = []
		self.feed(urllib2.urlopen(urllib2.Request(url)).read())
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "file":
			self.files.append(attrs[1][1])

class ServiceUpdate:
	""""""""
	def __init__(self):
		""""""
		self.config = config.Config() 

	def get_updates(self, local_services):
		""""""
		new_services = {}
		list = ServiceList(BASE)
		for remote_service in list.services:
			check = ServiceCheck(BASE + remote_service)
			found = False
			if CONF_FILE in check.files:
				#get remote version
				config = ServiceConfig(None, urllib2.urlopen(urllib2.Request(BASE + remote_service + CONF_FILE)))
				remote_version = config.get_update()
				#get local version
				for local_service in local_services:
					if local_service[0] == remote_service.split("/")[0]:
						found = True
						local_version = local_service[4].get_update()
						if remote_version > local_version:
							new_services[local_service[2]] = local_service[0], check.files, local_service[1]
			if not found:
				new_services[config.get_name()] = remote_service.split("/")[0], check.files, None
		return new_services

	def install_service(self, service_name, service_dir, files):
		""""""
		for file_name in files:
			handle = urllib2.urlopen(urllib2.Request("%s%s/%s" % (BASE, service_dir, file_name)))
			#windows incompatibility
			if "text" in handle.info()["Content-Type"]:
				write_mode = "w"
			else:
				write_mode = "wb"
			if not os.path.isdir(os.path.join(cons.PLUGIN_PATH, service_dir)):
				os.mkdir(os.path.join(cons.PLUGIN_PATH, service_dir))
			print "Updating: ", os.path.join(cons.PLUGIN_PATH, service_dir, file_name)
			f = file(os.path.join(cons.PLUGIN_PATH, service_dir, file_name), write_mode)
			f.write(handle.read())
			f.close()
			if not self.config.has_option(config.SECTION_SERVICES, service_name):
				self.config.set(config.SECTION_SERVICES, service_name, os.path.join(cons.PLUGIN_PATH, service_dir, ""))

if __name__ == "__main__":
	s = ServiceUpdate()
	updates = s.get_updates(Config().get_services())
	print updates
	service, files, icon = updates["megaupload.com"]
	s.install_service(service, files)
