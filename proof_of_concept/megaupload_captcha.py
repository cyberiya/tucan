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

from tesseract import Tesseract

import urllib2

from HTMLParser import HTMLParser

class CaptchaParser(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.located = False
		self.captcha = None
		self.feed(urllib2.urlopen(urllib2.Request(url)).read())
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "td":
			if self.get_starttag_text() == '<TD width="100" align="center" height="40">':
				self.located = True
		elif tag == "img":
			if self.located:
				self.located = False
				self.captcha = attrs[0][1]

class Captcha:
	""""""
	def __init__(self, data):
		""""""
		self.tess = Tesseract(data, self.filter)
		
	def get_captcha(self):
		result = self.tess.get_captcha()
		if len(result) == 4:
			return result
		
	def filter(self, data):
		""""""
		return data

if __name__ == "__main__":
	
	link = None
	while not link:
		p = CaptchaParser("http://www.megaupload.com/es/?d=RDAJ2PYH")
		if p.captcha:
			print p.captcha
			c = Captcha(urllib2.urlopen(urllib2.Request(p.captcha)).read())
			captcha = c.get_captcha()
			if captcha:
				link = captcha
	print link