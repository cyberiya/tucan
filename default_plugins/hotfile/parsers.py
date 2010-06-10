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
import logging
logger = logging.getLogger(__name__)

from HTMLParser import HTMLParser

import ImageOps

from core.tesseract import Tesseract
from core.url_open import URLOpen

BASE_URL = "http://hotfile.com"

class CaptchaParser(HTMLParser):
	def __init__(self, url, form):
		""""""
		HTMLParser.__init__(self)
		self.link = None
		self.action_captcha = None
		self.captchaid = None
		self.hash1 = None
		self.hash2 = None
		self.captcha_url = None
		try:
			opener = URLOpen()
			tmp = opener.open(url, form).readlines()
			for line in tmp:
				self.feed(line)
				self.close()
			if self.action_captcha:
				tes = Tesseract(opener.open(self.captcha_url).read(), self.filter_image)
				captcha = tes.get_captcha()
				logger.warning("Captcha: %s" % captcha)
				form = urllib.urlencode([("action", self.action_captcha), ("captchaid", self.captchaid), ("hash1", self.hash1), ("hash2", self.hash2), ("captcha", captcha)])
				tmp = opener.open(url, form).readlines()
			for line in tmp:
				if '<table class="downloading"><tr><td>Downloading <b>' in line:
					if "href" in line:
						tmp = line.split('<a href="')[1].split('">')[0].split("/")
						tmp.append(urllib.quote(tmp.pop()))
						self.link = "/".join(tmp)
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "input":
			if ("name", "action") in attrs:
				for ref, value in attrs:
					if ref == "value" and value == "checkcaptcha":
						self.action_captcha = value
			elif ("name", "captchaid") in attrs:
				for ref, value in attrs:
					if ref == "value":
						self.captchaid = value
			elif ("name", "hash1") in attrs:
				for ref, value in attrs:
					if ref == "value":
						self.hash1 = value
			elif ("name", "hash2") in attrs:
				for ref, value in attrs:
					if ref == "value":
						self.hash2 = value
		elif tag == "img":
			self.captcha_url = "%s%s" % (BASE_URL, attrs[0][1])

	def filter_image(self, image):
		""""""
		image = image.point(self.filter_pixel)
		image = ImageOps.grayscale(image)
		return image

	def filter_pixel(self, pixel):
		""""""
		if pixel > 110:
			return 255
		if pixel > 90:
			return 100
		else:
			return 1

class Parser:
	def __init__(self, url):
		""""""
		self.link = None
		self.wait = None
		found = False
		form = []
		try:
			opener = URLOpen()
			for line in opener.open(url).readlines():
				if "download_file" in line:
					found = True
				elif found:
					if "method=post " in line:
						self.link = "%s%s" % (BASE_URL, line.split('action="')[1].split('" ')[0])
					elif "name=action " in line:
						form.append(("action", line.split("value=")[1].split(">")[0]))
					elif "name=tm " in line:
						form.append(("tm", line.split("value=")[1].split(">")[0]))
					elif "name=tmhash " in line:
						form.append(("tmhash", line.split("value=")[1].split(">")[0]))
					elif "name=wait " in line:
						self.wait = int(line.split("value=")[1].split(">")[0])
						form.append(("wait", self.wait))
					elif "name=waithash " in line:
						form.append(("waithash", line.split("value=")[1].split(">")[0]))
					elif "name=upidhash " in line:
						form.append(("upidhash", line.split("value=")[1].split(">")[0]))
						found = False
			self.form = urllib.urlencode(form)
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			for line in URLOpen().open(url).readlines():
				if 'class="arrow_down"' in line:
					tmp = line.split("</strong>")
					name = tmp[1].split("<span>")[0].strip()
					tmp = tmp[1].split("<strong>")[1].split(" ")
					size = int(round(float(tmp[0])))
					unit = tmp[1].upper()
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	#print CheckLinks().check("http://hotfile.com/dl/7174149/00fbb47/Sander_Van_Doorn-Live_at_Sensation_White_Saint-Petersburg-12062009.mp3.html")
	c = Parser("http://hotfile.com/dl/7174149/00fbb47/Sander_Van_Doorn-Live_at_Sensation_White_Saint-Petersburg-12062009.mp3.html")
	print c.link
	print c.form, c.wait
	import time
	for i in range(c.wait):
		print i
		time.sleep(1)
	for line in URLOpen().open(c.link, c.form).readlines():
		if "click_download" in line:
			print line.split('href="')[1].split('"')[0]
			break
		elif "checkcaptcha" in line:
			print line
			break
	#m = CaptchaParser(c.link, c.form)
	#print m.link
