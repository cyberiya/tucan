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

from HTMLParser import HTMLParser

from core.tesseract import Tesseract
from core.url_open import URLOpen

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
		try:
			opener = URLOpen(cookie)
			if "/file/" in url:
				tmp = url.split("file/")
				url = "%s?%s" % (tmp[0], tmp[1].split("/")[0])
			elif "download.php" in url:
				url = "".join(url.split("download.php"))
			for line in opener.open(url).readlines():
				if "cu(" in line:
					if "GetCaptcha" in line:
						print line
						logger.warning("Unable to solve Recaptcha")
					else:
						tmp = line.split("cu('")[1].split("');")[0].split("','")
						handle = opener.open("http://www.mediafire.com/dynamic/download.php?%s" % (urllib.urlencode([("qk", tmp[0]), ("pk", tmp[1]), ("r", tmp[2])])))
						tmp = handle.readlines()
						vars = {}

						sum = tmp[1].split("+mL+'/' ")[1].split(" 'g/'")[0]
						server = tmp[1].split("mL='")[1].split("';")[0]
						link = tmp[1].split("mH='")[1].split("';")[0]
						name = tmp[1].split("mY='")[1].split("';")[0]
						
						for var in tmp[1].split(";"):
							var = var.split("var")
							if len(var) > 1:
								var = var[1].strip().split("=")
								if ((len(var) > 1) and ("'" in var[1])):
									vars[var[0]] = var[1].split("'")[1]
						for var in sum.split("+"):
							if len(var) > 0:
								if var in vars.keys():
									random += vars[var]
								else:
									error = True
		except Exception, e:
			error = True
			logger.exception("%s: %s" % (url, e))
		if server and random and link and name and not error:
			self.url = "http://%s/%sg/%s/%s" % (server, random, link, name)

class CheckLinks(HTMLParser):
	""""""
	def check(self, url):
		""""""
		self.name = url
		self.size = 0
		self.unit = None
		try:
			if "/file/" in url:
				tmp = url.split("file/")
				url = "%s?%s" % (tmp[0], tmp[1].split("/")[0])
			elif "download.php" in url:
				url = "".join(url.split("download.php"))
			for line in URLOpen().open(url).readlines():
				if self.size and self.unit:
					break
				else:
					self.feed(line)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		return self.name, self.size, self.unit

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "input":
			if attrs[1][1] == "sharedtabsfileinfo1-fn":
				self.name = attrs[2][1]
			elif attrs[1][1] == "sharedtabsfileinfo1-fs":
				tmp = attrs[2][1].split(" ")
				self.size = int(float(tmp[0]))
				self.unit = tmp[1]

if __name__ == "__main__":
	f = FormParser("http://www.mediafire.com/?ja1mn1gz1ji", cookielib.CookieJar())
	print f.url
	#print CheckLinks().check("http://www.mediafire.com/download.php?z0gjmnwk1d0")
	#print CheckLinks().check("http://www.mediafire.com/?0ojmelsgdn4")
	#print CheckLinks().check("http://www.mediafire.com/?mnqzmm5dm0g")
