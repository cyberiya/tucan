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

import math
import urllib2

from HTMLParser import HTMLParser
		
class PremiumParser(HTMLParser):
	""""""
	def __init__(self, url, cookie):
		""""""
		HTMLParser.__init__(self)
		self.located = False
		self.url = None
		self.size = None
		for line in urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)).open(urllib2.Request(url)).readlines():
			self.feed(line)
			if "File size:" in line:
				self.size = line.strip()
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "div":
			if ((len(attrs) > 1) and (attrs[1][1] == "downloadlink")):
				self.located = True
		elif tag == "a":
			if self.located:
				self.located = False
				self.url = attrs[0][1]
		
	def get_url(self):
		""""""
		return self.url
		
	def check_link(self):
		""""""
		name = None
		size = 0
		unit = None
		if self.url:
			name = self.url.split("/").pop()
		if self.size:
			tmp = self.size.split("</font>")
			tmp.pop()
			tmp = tmp.pop()
			tmp = tmp.split(">").pop().split(" ")
			size = int(float(tmp[0]))
			unit = tmp[1]
		return name, size, unit
		
if __name__ == "__main__":
	from premium_cookie import PremiumCookie
	c = PremiumCookie()
	p = PremiumParser("http://www.megaupload.com/?d=RDAJ2PYH", c.get_cookie("",""))
	print p.get_url()
	print p.check_link()
