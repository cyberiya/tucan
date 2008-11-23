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

import urllib2

from .anonymous_plugin import AnonymousPlugin

NAME = "Megaupload Anonimo"
VERSION = "0.1"
AUTHOR = "Crak"

SERVICE = "megaupload.com"
DOWNLOAD_SLOTS = 1
UPLOAD_SLOTS = 1

class AnonymousMegaupload(AnonymousPlugin):
	""""""
	def __init__(self):
		""""""
		AnonymousPlugin.__init__(self, DOWNLOAD_SLOTS, UPLOAD_SLOTS)
		self.__name__ = NAME
		self.__version__ = VERSION
		self.__author__ = AUTHOR
		self.service = SERVICE

	def check_link(self, url):
		""""""
		name = None
		size = 0
		unit = None
		for line in urllib2.urlopen(urllib2.Request(url)).readlines():
			if "<b>Filename:</b>" in line:
				name = line.split("<b>Filename:</b>")[1].split("</div>")[0].strip()
			elif "<b>Filesize:</b>" in line:
				tmp = line.split("<b>Filesize:</b>")[1].split("</div>")[0].split(" ")
				size = int(round(float(tmp[1])))
				unit = tmp[2]
		return name, size, unit