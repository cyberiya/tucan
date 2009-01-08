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

import math
import urllib
import urllib2

from HTMLParser import HTMLParser

import Image
import ImageOps

from tesseract import Tesseract

class CaptchaForm:
	""""""
	def __init__(self, url):
		""""""
		self.url = url
		self.link = None
		cont = 0
		while not self.link and cont < 10:
			self.get_link()
			cont += 1
		print self.link

	def get_link(self):
		""""""
		c_parser = CaptchaParser(self.url)
		if ((c_parser.form_action) and (c_parser.captcha)):
			handle = urllib2.urlopen(urllib2.Request(c_parser.form_action + c_parser.captcha))
			tes = Tesseract(handle.read(), self.filter_image)
			handle.close()
			self.captcha = tes.get_captcha()
			if len(self.captcha) == 3:
				form = {"d": c_parser.form_d, "imagecode": c_parser.form_imagecode, "megavar": c_parser.form_megavar, "imagestring" : self.captcha.strip()}
				data = urllib.urlencode(form)
				handle = urllib2.urlopen(c_parser.form_action, data)
				u_parser = UrlParser(handle.read())
				handle.close()
				if  u_parser.tmp_url:
					self.link = u_parser.get_url()
	def filter_image(self, image):
		""""""
		image = image.resize((140,64), Image.BICUBIC)
		image = ImageOps.grayscale(image)
		return image

class CaptchaParser(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.captcha = None
		self.form_action = None
		self.form_d = None
		self.form_imagecode = None
		self.form_megavar = None
		self.feed(urllib2.urlopen(urllib2.Request(url)).read())
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "img":
			if attrs[0][0]  == "src":
				if attrs[0][1].find("capgen") > 0:
					self.captcha = attrs[0][1]
		elif tag == "form":
			if attrs[0][1] == "POST":
				self.form_action = attrs[1][1]
		elif tag == "input":
			if attrs[1][1] == "d":
				self.form_d = attrs[2][1]
			if attrs[1][1] == "imagecode":
				self.form_imagecode= attrs[2][1]
			if attrs[1][1] == "megavar":
				self.form_megavar = attrs[2][1]
		
class UrlParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.tmp_url = None
		self.url_pos = None
		self.data = data
		self.feed(self.data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ('class', 'downloadhtml') in attrs:
				self.url_pos = self.getpos()
			elif  ('onclick', 'loadingdownload();') in attrs:
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
