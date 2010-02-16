###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
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

import urllib
import cookielib
import logging
logger = logging.getLogger(__name__)

from core.url_open import URLOpen

GET_URL = "http://www.storage.to/getlink/"

class Parser:
	def __init__(self, url):
		""""""
		self.link = None
		self.wait = 0
		self.cookie = cookielib.CookieJar()
		try:
			opener = URLOpen(self.cookie)
			for line in opener.open(url).readlines():
				if "javascript:startcountdown" in line:
					id = line.split("(")[1].split(")")[0].split(",")[2].split('"')[1]
					tmp = opener.open("%s%s/" % (GET_URL, id)).read().split("{")[1].split("}")[0].split(",")
					if tmp[0].split(" : ")[1] == "'ok'":
						self.wait = int(tmp[1].split(" : ")[1])
						self.link = tmp[2].split(" : ")[1].split("'")[1]
					break
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = url
		size = 0
		unit = None
		index = 0
		try:
			tmp = URLOpen().open(url).readlines()
			for line in tmp:
				if "download_container" in line:
					index = tmp.index(line)
			if index > 0:
				tmp = tmp[index+2].split("</span>")[1].split('<span class="light">')
				name = tmp[0].strip()
				size = int(float(tmp[1].split("(")[1].split(" ")[0]))
				unit = tmp[1].split(" ")[1].split(")")[0]
		except Exception, e:
			name = url
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	#c = Parser("http://www.storage.to/get/3P9jKCnn/")
	#print c.link
	print CheckLinks().check("http://www.storage.to/get/l0Z8Us4c/")
