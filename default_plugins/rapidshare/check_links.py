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

import cons

class CheckLinks:
	""""""	
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in urllib2.urlopen(urllib2.Request(url)).readlines():
				if "downloadlink" in line:
					tmp = line.split(">")
					name = tmp[1].split("<")[0].strip().split("/").pop()
					size = int(tmp[2].split("<")[0].split(" ")[1])
					unit = tmp[2].split("<")[0].split(" ")[2]
					if unit == cons.UNIT_KB:
						size = int(size/1024)
						unit = cons.UNIT_MB
		except urllib2.URLError, e:
			print e
		return name, size, unit
