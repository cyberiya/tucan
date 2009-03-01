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

import urllib
import urllib2
import cookielib

#import cons

class FormParser:
	""""""
	def __init__(self, url, cookie):
		""""""
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		for line in opener.open(urllib2.Request(url)).readlines():
			if "cu(" in line:
				tmp = eval(line.split("cu(")[1].split(");")[0])
				handle = opener.open(urllib2.Request("http://www.mediafire.com/dynamic/download.php"), urllib.urlencode({"qk": tmp[0], "pk": tmp[1], "r": tmp[2]}))
				print handle.read()


class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None			
		for line in urllib2.urlopen(urllib2.Request(url)).readlines():
			if "You requested:" in line:
				tmp = line.split("You requested:")[1].split("</div>")[0].strip().split(" ")
				name = tmp[0]
				size = int(float(tmp[1].split("(")[1]))
				unit = tmp[2].split(")")[0]
			if not name:
				name = url
				size = -1
		return name, size, unit

if __name__ == "__main__":
	f = FormParser("http://www.mediafire.com/?vdmjzmyquyj", cookielib.CookieJar())