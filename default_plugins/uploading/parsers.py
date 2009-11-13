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
import cookielib
import logging
logger = logging.getLogger(__name__)

from HTMLParser import HTMLParser

from core.url_open import URLOpen

JS_URL = "http://uploading.com/files/get/?JsHttpRequest=0-xml"

class Parser(HTMLParser):
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.form_action = None
		self.link_id = None
		self.link = url
		self.wait = 60
		self.opener = URLOpen(cookielib.CookieJar())
		try:
			for line in self.opener.open(url).readlines():
				self.feed(line)
			self.close()
			data = urllib.urlencode([("action", "second_page"), ("file_id", self.link_id)])
			if self.form_action:
				self.opener.open(self.form_action, data).read()
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
			
	def get_handler(self):
		""""""
		try:
			data = urllib.urlencode([("action", "get_link"), ("file_id", self.link_id), ("pass", "undefined")])
			tmp = self.opener.open(JS_URL, data).read()
			if '{ "id": "0", "js": { "answer": { "link": "' in tmp:
				link = urllib.unquote(tmp.split(' "id": "0", "js": { "answer": { "link": "')[1].split('" }')[0]).replace("\\", "")
				return self.opener.open(link)
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if attrs[2][1] == "downloadform":
				self.form_action = attrs[0][1]
		elif tag == "input":
			if attrs[1][1] == "file_id":
				self.link_id = attrs[2][1]

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = url
		size = 0
		unit = None
		index = 0
		try:
			tmp = URLOpen().open(url).readlines()
			for line in tmp:
				if '<div class="c_1">' in line:
					index = tmp.index(line)
			if "<h2>" in tmp[index+2]:
				name = tmp[index+2].split("<h2>")[1].split("</h2>")[0]
				tmpsize = tmp[index+3].split("<b>")[1].split("</b>")[0].split(" ", 1)
				size = int(float(tmpsize[0]))
				unit = tmpsize[1].strip().upper()
		except Exception, e:
			name = url
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	c = Parser("http://uploading.com/files/MQJ6TLCW/")
	import time
	time.sleep(60)
	print c.get_handler()
	#print CheckLinks().check("http://uploading.com/files/MQJ6TLCW/")
