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

import logging
logger = logging.getLogger(__name__)

import HTMLParser

from url_open import URLOpen

class Parser(HTMLParser.HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.HTMLParser.__init__(self)
		self.tmp_link = None
		self.link = None
		try:
			opener = URLOpen()
			for line in opener.open(url).readlines():
				if "get" in line:
					try:
						self.feed(line)
					except HTMLParser.HTMLParseError, e:
						logger.warning("%s :%s %s" % (url, line.strip(), e))
			if self.tmp_link:
				for line in opener.open(self.tmp_link).readlines():
					if "Click here to download this file" in line:
						self.link = line.split("<a href='")[1].split("'>")[0]
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ((len(attrs) == 3) and (attrs[1][1] == "dbtn")):
				self.tmp_link = attrs[0][1]

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		size_found = False
		for line in URLOpen().open(url).readlines():
			if "fileNameText" in line:
				name = line.strip().split(">")[1].split("<")[0]
			elif "Size" in line:
				size_found = True
			elif size_found:
				size_found = False
				tmp = line.strip().split(">")[1].split("<")[0]
				unit = tmp.split(" ")[1]
				if "," in tmp:
					size = int("".join(tmp.split(" ")[0].split(",")))
				else:
					size = int(tmp.split(" ")[0])
				if size > 1024:
					if unit == "KB":
						size = size/1024
						unit = "MB"
		if not name:
			name = url
			size = -1
		return name, size, unit

if __name__ == "__main__":
	c = Parser("http://www.4shared.com/file/91343636/4fa0632e/AF_Shamo_-_13_-_130.html")
	#print CheckLinks().check("http://www.4shared.com/file/91343636/4fa0632e/AF_Shamo_-_13_-_130.html")