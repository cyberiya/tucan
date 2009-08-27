###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crak@tucaneando.com
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
import logging
logger = logging.getLogger(__name__)

from HTMLParser import HTMLParser

import sys
sys.path.append("/Users/Crak/Desktop/tucan-osx/trunk")

from url_open import URLOpen, set_proxy

set_proxy(None)

BASE_URL = "http://hotfile.com"

class Parser(HTMLParser):
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.link = None
		self.form = None
		self.tm = None
		self.tmhash = None
		self.waithash = None
		self.wait = None
		try:
			opener = URLOpen()
			self.feed(opener.open(url).read())
			self.close()
			self.form = urllib.urlencode([("action", "capt"), ("tm", self.tm), ("tmhash", self.tmhash), ("wait", self.wait), ("waithash", self.waithash)])
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

	def handle_starttag(self, tag, attrs):
		""""""
		if self.link:
			if tag == "input":
				if ("name", "tm") in attrs:
					for ref, value in attrs:
						if ref == "value":
							self.tm = value
				elif ("name", "tmhash") in attrs:
					for ref, value in attrs:
						if ref == "value":
							self.tmhash = value
				elif ("name", "wait") in attrs:
					for ref, value in attrs:
						if ref == "value":
							self.wait = int(value)
				elif ("name", "waithash") in attrs:
					for ref, value in attrs:
						if ref == "value":
							self.waithash = value
		else:
			if tag == "form":
				if len(attrs) > 3:
					self.link = "%s%s" % (BASE_URL, attrs[1][1])

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in URLOpen().open(url).readlines():
				if '<table class="downloading">' in line:
					name = line.split('Downloading <b>')[1].split('</b>')[0]
					tmp = line.split('<span class="size">|')[1].strip().split('</span>')[0]
					unit = tmp[-2:].upper()
					size = int(round(float(tmp[:-2])))
			if not unit:
				name = url
				size = -1
		except Exception, e:
			name = url
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	c = Parser("http://hotfile.com/dl/10804393/9f439e8/Bruno_-_www.crostuff.net.part1.rar.html")
	#print CheckLinks().check("http://hotfile.com/dl/10804393/9f439e8/Bruno_-_www.crostuff.net.part1.rar.html")
