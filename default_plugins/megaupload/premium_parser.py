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
		self.tmp_url = None
		self.url_pos = None
		self.data = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)).open(urllib2.Request(url)).read()
		self.feed(self.data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ('class', 'downloadhtml') in attrs:
				if not self.url_pos:
					self.url_pos = self.getpos()
				else:
					self.tmp_url = attrs[0][1]
		
	def get_url(self):
		""""""
		vars = {}
		data = self.data.split("\n")
		tmp = data[self.url_pos[0]].split(" ")
		vars[tmp[1]] = chr(int(tmp[3].split("-")[1].split(")")[0]))

		tmp = data[self.url_pos[0]+1].split(" ")
		vars[tmp[1]] = tmp[3].split("\'")[1] + chr(int(math.sqrt(int(tmp[5].split("sqrt(")[1].split(")")[0]))))
		tmp = self.tmp_url.split(" + ")
		return tmp[0].split("\'")[0] + vars[tmp[1]] + vars[tmp[2]] + tmp[3].split("\'")[1]
