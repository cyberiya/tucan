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

import Image

from HTMLParser import HTMLParser

from tesseract import Tesseract

CAPTCHACODE = "captchacode"
MEGAVAR = "megavar"

class CheckLinks(HTMLParser):
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in urllib2.urlopen(urllib2.Request(url)).readlines():
				if "Filename:" in line:
					name = line.split(">")[3].split("</")[0].strip()
				elif "File size:" in line:
					tmp = line.split(">")[3].split("</")[0].split(" ")
					size = int(round(float(tmp[0])))
					unit = tmp[1]
			if name:
				if ".." in name:
					parser = CaptchaForm(url)
					if parser.link:
						name = parser.link.split("/").pop()
		except urllib2.URLError, e:
			print e
		return name, size, unit

class CaptchaParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.located = False
		self.captcha = None
		self.captchacode = ""
		self.megavar = ""
		self.feed(data)
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
		elif tag == "input":
			if attrs[1][1] == CAPTCHACODE:
				self.captchacode = attrs[2][1]
			elif attrs[1][1] == MEGAVAR:
				self.megavar = attrs[2][1]

class CaptchaForm(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.link = None
		self.located = False
		while not self.link:
			p = CaptchaParser(urllib2.urlopen(urllib2.Request(url)).read())
			if p.captcha:
				print p.captcha
				handle = urllib2.urlopen(urllib2.Request(p.captcha))
				if handle.info()["Content-Type"] == "image/gif":
					self.tess = Tesseract(handle.read(), self.filter)
					captcha = self.get_captcha()
					if captcha:
						handle = urllib2.urlopen(urllib2.Request(url), urllib.urlencode([(CAPTCHACODE, p.captchacode), (MEGAVAR, p.megavar), ("captcha", captcha)]))
						self.reset()
						self.feed(handle.read())
						self.close()
						print captcha
		
	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ((self.located) and (attrs[0][0] == "href")):
				self.located = False
				self.link = attrs[0][1]
		elif tag == "div":
			if ((len(attrs) > 1) and (attrs[1][1] == "downloadlink")):
				self.located = True

	def get_captcha(self):
		result = self.tess.get_captcha()
		if len(result) == 4:
			return result
		
	def filter(self, im):
		""""""
		x_size, y_size = im.size
		d1 =      0 + ((x_size / 4) + 8)
		d2 =      0 + ((x_size / 4) - 1)
		d3 =     d2 + ((x_size / 4) + 8)
		d4 =      0 + ((x_size / 2) - 4)
		d5 =     d4 + ((x_size / 4) + 8)
		d6 = x_size - ((x_size / 4) + 5)
		im1 = im.crop(( 0, 0,     d1, y_size))
		im2 = im.crop((d2, 0,     d3, y_size))
		im3 = im.crop((d4, 0,     d5, y_size))
		im4 = im.crop((d6, 0, x_size, y_size))

		angle = 26
		filter = Image.BICUBIC
		im1 = im1.rotate(+angle, filter, 1)
		im2 = im2.rotate(-angle, filter, 1)
		im3 = im3.rotate(+angle, filter, 1)
		im4 = im4.rotate(-angle, filter, 1)
		data = Image.new("L", (im1.size[0] + im2.size[0] + im3.size[0] + im4.size[0], im1.size[1]), None)
		data.paste(im1, (0, 0))
		data.paste(im2, (im1.size[0], 0))
		data.paste(im3, (im1.size[0] + im2.size[0], 0))
		data.paste(im4, (im1.size[0] + im2.size[0] + im3.size[0], 0))
		return data

if __name__ == "__main__":
	c = CaptchaForm("http://www.megaupload.com/?d=RDAJ2PYH")
	print c.link
	#print CheckLinks().check("http://www.megaupload.com/?d=1UY9LV7O")
	