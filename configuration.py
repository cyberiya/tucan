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

import cons

DEFAULT_PATH = cons.DEFAULT_PATH + ".tucan/"
CONF = "tucan.conf"

COMMENT = """# Tucan Manager's default configuration.
# Dont change anything unless you really know what are doing, 
# instead use the preferences dialog of the GUI."""

DEFAULTS = {"main": {"language": "English", "max_downloads": "5", "max_uploads": "5", "downloads_folder": cons.DEFAULT_PATH}
	, "services": {}
	, "advanced": {"tray_close": "True", "advanced_packages": "True"}}

class Configuration(SafeConfigParser):
	""""""
	def __init__(self):
		""""""
		SafeConfigParser.__init__(self)
		if not os.path.exists(DEFAULT_PATH):
			os.mkdir(DEFAULT_PATH)
		if not os.path.exists(DEFAULT_PATH + CONF):
			self.create_config()
		else:
			self.read(DEFAULT_PATH + CONF)
			if not self.check_config():
				self.create_config()

	def check_config(self):
		""""""
		for section, options in DEFAULTS.items():
			if self.has_section(section):
				for option, value in self.items(section):
					if not option in options:
						return False
			else:
				return False
		
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
		
if __name__ == "__main__":
	c = Configuration()
