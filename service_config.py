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
import pickle

from ConfigParser import SafeConfigParser

import cons

SECTION_MAIN = "main"
SECTION_DOWNLOADS = "downloads"
SECTION_UPLOADS = "uploads"

SECTION_ANONYMOUS_DOWNLOAD = "anonymous_download"
SECTION_USER_DOWNLOAD = "user_download"
SECTION_PREMIUM_DOWNLOAD = "premium_download"

SECTION_ANONYMOUS_UPLOAD = "anonymous_upload"
SECTION_USER_UPLOAD = "user_upload"
SECTION_PREMIUM_UPLOAD = "premium_upload"

OPTION_NAME = "name"
OPTION_ICON = "icon"
OPTION_ENABLED = "enabled"

OPTION_AVAIBLE = "avaible"
OPTION_CHECK_LINKS = "check_links"
OPTION_CHECK_FILES = "check_files"

OPTION_PATH = "path"
OPTION_NAME = "name"
OPTION_AUTHOR = "author"
OPTION_VERSION = "version"
OPTION_SLOTS = "slots"
OPTION_CAPTCHA = "captcha"
OPTION_ACCOUNTS = "accounts"

CONF = "service.conf"

class ServiceConfig(SafeConfigParser):
	""""""
	def __init__(self, path):
		""""""
		SafeConfigParser.__init__(self)
		self.path = path
		if os.path.exists(self.path + CONF):
			self.read(self.path + CONF)
	
	def check_config(self):
		""""""
		result = True
		for section in [SECTION_MAIN, SECTION_DOWNLOADS, SECTION_UPLOADS]:
			if not self.has_section(section):
				result = False
		return result
		
	def enable(self, enabled):
		""""""
		self.set(SECTION_MAIN, OPTION_ENABLED, str(enabled))
		self.save()

	def get_icon(self):
		""""""
		if self.has_option(SECTION_MAIN, OPTION_ICON):
			if not self.get(SECTION_MAIN, OPTION_ICON) == "None":
				return self.path + self.get(SECTION_MAIN, OPTION_ICON)
				
	def get_plugins(self):
		""""""
		result = {}
		if self.has_section(SECTION_DOWNLOADS):
			if self.getboolean(SECTION_DOWNLOADS, OPTION_AVAIBLE):
				downloads = []
				if ((self.has_section(SECTION_ANONYMOUS_DOWNLOAD)) and (len(self.items(SECTION_ANONYMOUS_DOWNLOAD)) > 0)):
					downloads.append((SECTION_ANONYMOUS_DOWNLOAD, cons.TYPE_ANONYMOUS))
				if ((self.has_section(SECTION_USER_DOWNLOAD)) and (len(self.items(SECTION_USER_DOWNLOAD)) > 0)):
					downloads.append((SECTION_USER_DOWNLOAD, cons.TYPE_USER))
				if ((self.has_section(SECTION_PREMIUM_DOWNLOAD)) and (len(self.items(SECTION_PREMIUM_DOWNLOAD)) > 0)):
					downloads.append((SECTION_PREMIUM_DOWNLOAD, cons.TYPE_PREMIUM))
				if len(downloads) > 0:
					result[SECTION_DOWNLOADS] = downloads
		if self.has_section(SECTION_UPLOADS):
			if self.getboolean(SECTION_UPLOADS, OPTION_AVAIBLE):
				uploads = []
				if ((self.has_section(SECTION_ANONYMOUS_UPLOAD)) and (len(self.items(SECTION_ANONYMOUS_UPLOAD)) > 0)):
					uploads.append((SECTION_ANONYMOUS_UPLOAD, cons.TYPE_ANONYMOUS))
				if ((self.has_section(SECTION_USER_UPLOAD)) and (len(self.items(SECTION_USER_UPLOAD)) > 0)):
					uploads.append((SECTION_USER_UPLOAD, cons.TYPE_USER))
				if ((self.has_section(SECTION_PREMIUM_UPLOAD)) and (len(self.items(SECTION_PREMIUM_UPLOAD)) > 0)):
					uploads.append((SECTION_PREMIUM_UPLOAD, cons.TYPE_PREMIUM))
				if len(uploads) > 0:
					result[SECTION_UPLOADS] = uploads
		return result

	def get_accounts(self, section):
		""""""
		result = {}
		if self.has_section(section):
			if os.path.exists(self.path + self.get(section, OPTION_ACCOUNTS)):
				f = open(self.path + self.get(section, OPTION_ACCOUNTS))
				result = pickle.load(f)
				f.close()
		return result

	def set_accounts(self, section, accounts):
		""""""
		if self.has_section(section):
			f = open(self.path + self.get(section, OPTION_ACCOUNTS), "w")
			pickle.dump(accounts, f)
			f.close()

	def save(self):
		""""""
		f = open(self.path + CONF, "w")
		self.write(f)
		f.close()

if __name__ == "__main__":
	c = ServiceConfig("/home/crak/.tucan/plugins/megaupload/")
