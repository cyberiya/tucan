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

import sys
sys.path.append("/home/crak/tucan/trunk")
import __builtin__
__builtin__.PROXY = None

from core.url_open import URLOpen

class FormParser:
	""""""
	def __init__(self, url, cookie):
		""""""
		self.url = None
		error = False
		try:
			if "/file/" in url:
				tmp = url.split("file/")
				url = "%s?%s" % (tmp[0], tmp[1].split("/")[0])
			elif "download.php" in url:
				url = "".join(url.split("download.php"))
			while not self.url and not error:
				opener = URLOpen(cookie)
				for line in opener.open(url).readlines():
					if "function RunOnLoad()" in line:
						tmp_link = None
						tmp = line.split("Eo();")[1].strip()
						if tmp.startswith("GetCaptcha("):
							logger.warning("Unable to solve Recaptcha")
							error = True
						elif not tmp.startswith("eval("):
							eval_var = tmp.split(";", 1)[0].split("=''")[0]
							tmp_link = self.decode(tmp, eval_var)
							if tmp_link:
								tmp = tmp_link.split("(")[1].split(")")[0].split(",")
								data = urllib.urlencode([("qk", tmp[0].split("'")[1]), ("pk", tmp[1].split("'")[1]), ("r", tmp[2].split("'")[1])])
								print data
								while not self.url:
									handle = opener.open("http://www.mediafire.com/dynamic/download.php?%s" % data)
									tmp = handle.readlines()
									if "var et= 15;" in tmp[1]:
										for line in tmp[2:]:
											if "%22http%3A%2F%2Fdownload" in line:
												tmp_link = urllib.unquote(line)
												tmp_link = tmp_link.split('href=\\"')[1].split('\\">')[0]
												server = tmp_link.split('" +')[0]
												random_var = tmp_link.split('" +')[1].split('+ "')[0]
												name = tmp_link.split('+ "')[1]
												tmp = tmp[1].split("function dz()")[0]											
												eval_var = tmp.split(";", 3)[2].split("=''")[0].strip()
												tmp = self.decode(tmp, eval_var, True)
												for var in tmp.split(";"):
													if random_var in var:
														self.url = "%s%s%s" % (server, var.split("'")[1], name)
												break
						break
		except Exception, e:
			error = True
			logger.exception("%s: %s" % (url, e))
			
	def decode(self, data, eval_var, unlimited=False):
		""""""
		result = ""
		tmp = data.split("unescape('")[1].split("eval(%s);" % eval_var)[0].split(";")
		if len(tmp) > 5:
			posible_link = urllib.unquote(tmp[0].split("')")[0])
			iterations = int(tmp[1].split("=")[1])
			x = tmp[4].split("charCodeAt(i)")[1].split("))")[0].split("^")[1:]
			if iterations < 150 or unlimited:
				for i in range(iterations):
					t = ord(posible_link[i])
					for i in x:
						t = t ^ int(i)
					result += chr(t)
				return result


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
	f = FormParser("http://www.mediafire.com/?w4nzxzm0zg3", cookielib.CookieJar())
	#f = FormParser("http://www.mediafire.com/?5gbmmdds5bd", cookielib.CookieJar())
	print f.url
	#print CheckLinks().check("http://www.mediafire.com/download.php?z0gjmnwk1d0")
	#print CheckLinks().check("http://www.mediafire.com/?5gbmmdds5bd")
	#print CheckLinks().check("http://www.mediafire.com/?w4nzxzm0zg3")
