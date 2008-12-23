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

import os

from ConfigParser import SafeConfigParser

import service_config
import cons

DEFAULT_PATH = cons.DEFAULT_PATH + ".tucan/"
CONF = "tucan.conf"

COMMENT = """# Tucan Manager's default configuration.
# Dont change anything unless you really know what are doing, 
# instead use the preferences dialog of the GUI."""

SECTION_MAIN = "main"
SECTION_SERVICES = "services"
SECTION_ADVANCED = "advanced"

OPTION_LANGUAGE = "language"
OPTION_MAX_DOWNLOADS = "max_downloads"
OPTION_MAX_UPLOADS = "max_uploads"
OPTION_DOWNLOADS_FOLDER = "downloads_folder"

OPTION_TRAY_CLOSE = "tray_close"
OPTION_ADVANCED_PACKAGES = "advanced_packages"
OPTION_SHOW_UPLOADS = "show_uploads"

DEFAULTS = {SECTION_MAIN: {OPTION_LANGUAGE: "English", OPTION_MAX_DOWNLOADS: "5", OPTION_MAX_UPLOADS: "5", OPTION_DOWNLOADS_FOLDER: cons.DEFAULT_PATH}
	, SECTION_SERVICES: {}
	, SECTION_ADVANCED: {OPTION_TRAY_CLOSE: "False", OPTION_ADVANCED_PACKAGES: "False", OPTION_SHOW_UPLOADS: "False"}}

class Config(SafeConfigParser):
	""""""
	def __init__(self):
		""""""
		SafeConfigParser.__init__(self)
		self.configured = True
		if not os.path.exists(DEFAULT_PATH):
			os.mkdir(DEFAULT_PATH)
		if not os.path.exists(DEFAULT_PATH + CONF):
			self.create_config()
			self.configured = False
		else:
			self.read(DEFAULT_PATH + CONF)
			if not self.check_config():
				self.create_config()
				self.configured = False

	def check_config(self):
		""""""
		for section, options in DEFAULTS.items():
			if self.has_section(section):
				for option, value in options.items():
					if not option in [option for option, value in self.items(section)]:
						return False
			else:
				return False
		return True
		
	def create_config(self):
		""""""
		for section, options in DEFAULTS.items():
			if not self.has_section(section):
				self.add_section(section)
			for option, value in options.items():
				self.set(section, option, value)
		f = open(DEFAULT_PATH + CONF, "w")
		f.write(COMMENT + "\n\n")
		self.write(f)
		f.close()
		
	def get_services(self):
		""""""
		result = []
		for service, path in self.items(SECTION_SERVICES):
			config = service_config.ServiceConfig(path)
			if config.check_config():
				icon = config.get_icon()
				name = config.get(service_config.SECTION_MAIN, service_config.OPTION_NAME)
				enabled = config.getboolean(service_config.SECTION_MAIN, service_config.OPTION_ENABLED)
				result.append((icon, name, enabled, path, config))
		return result

	def save(self):
		""""""
		f = open(DEFAULT_PATH + CONF, "w")
		self.write(f)
		f.close()

if __name__ == "__main__":
	c = Config()
	print c.configured