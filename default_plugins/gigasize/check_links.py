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
from HTMLParser import HTMLParser

import cons

class CheckLinks(HTMLParser):
	""""""
	def __init__(self):
		""""""
		HTMLParser.__init__(self)
		self.active = False

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "div":
			if ((len(attrs) > 0) and (attrs[0][1] == "dldcontent")):
				self.active = True
	
	def close(self):
		HTMLParser.close(self)
		self.active = False

	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None			
		for line in urllib2.urlopen(url).readlines():
			if not self.active:
				self.feed(line)
			else:
				if "<p><strong>Name</strong>" in line:
					name = line.split("<b>")[1].split("</b>")[0].strip()
				elif "<p>Size:" in line:
					tmp = line.split("<span>")[1].split("</span>")[0].strip()
					if cons.UNIT_KB in tmp:
						unit = cons.UNIT_KB
						size = int(float(tmp.split(cons.UNIT_KB)[0]))
					elif cons.UNIT_MB in tmp:
						unit = cons.UNIT_MB
						size = int(float(tmp.split(cons.UNIT_MB)[0]))
					elif cons.UNIT_GB in tmp:
						unit = cons.UNIT_GB
						size = int(float(tmp.split(cons.UNIT_GB)[0]))
				if not "get.php?d=" in url:
					name = url.split("/").pop()
		self.close()
		return name, size, unit
