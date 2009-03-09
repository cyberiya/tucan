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
		self.url = None
		server = None
		random = ""
		link = None
		name = None
		error = False
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		for line in opener.open(urllib2.Request(url)).readlines():
			if "cu(" in line:
				tmp = eval(line.split("cu(")[1].split(");")[0])
				handle = opener.open(urllib2.Request("http://www.mediafire.com/dynamic/download.php?%s" %(urllib.urlencode([("qk", tmp[0]), ("pk", tmp[1]), ("r", tmp[2])]))))
				tmp = handle.readlines()
				vars = {}
				for var in tmp[1].split("function")[0].split(";"):
					var = var.split("var")
					if len(var) > 1:
						var = var[1].strip().split("=")
						if ((len(var) > 1) and ("'" in var[1])):
							value = var[1].split("'")[1]
							if var[0] == "mL":
								server = value
							elif var[0] == "mH":
								link = value
							elif var[0] == "mY":

								name = value
							else:
								vars[var[0]] = value
				try:
					sum = tmp[1].split("function")[1].split("Click here to start download..")[0]
					for var in sum.split("+mL+'/' +")[1].split("+ 'g/'+mH+'/'+mY+'")[0].split("+"):
						if var in vars.keys():
							random += vars[var]
						else:
							error = True
				except:
					print tmp
		if server and random and link and name and not error:
			self.url = "http://%s/%sg/%s/%s" % (server, random, link, name)

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
				unit = tmp.pop().split(")")[0]
				size = int(float(tmp.pop().split("(")[1]))
				name = "_".join(tmp)
			if not name:
				name = url
				size = -1
		return name, size, unit

if __name__ == "__main__":
	f = CheckLinks()
	print f.check("http://www.mediafire.com/?vdmjzmyquyj")