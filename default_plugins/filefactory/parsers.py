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
import logging
logger = logging.getLogger(__name__)

from HTMLParser import HTMLParser

import Image
import ImageFile #bug in PIL, using local file instead
import ImageOps

from tesseract import Tesseract
from url_open import URLOpen, set_proxy

BASE_URL = "http://www.filefactory.com%s"

class Parser(HTMLParser):
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.first_link = None
		self.link = None
		self.captcha_url = None
		self.captcha_id = None
		try:
			opener = URLOpen()
			self.feed(opener.open(url).read())
			if self.first_link:
				while not self.link:
					self.feed(opener.open(self.first_link).read())
					if self.captcha_url:
						logger.info("Captcha url: %s" % self.captcha_url)
						for i in range(25):
							self.image_string = URLOpen().open(self.captcha_url).read()
							tes = Tesseract(self.image_string, self.filter_image)
							captcha = tes.get_captcha()
							if len(captcha) == 4:
								logger.warning("Captcha: %s" % captcha)
								data = urllib.urlencode([("captchaID", self.captcha_id),("captchaText", captcha)])
								self.feed(URLOpen().open(self.first_link, data).read())
								if self.link:
									break
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
			
	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if attrs[0][1] == "download":
				self.first_link = BASE_URL % attrs[1][1]
			elif attrs[0][1] == "captchaReload ajax":
				self.captcha_url = BASE_URL % attrs[2][1]
			elif len(attrs) == 2 and attrs[1][1] == "download":
				self.link = attrs[0][1]
		elif tag == "input":
			if attrs[0][1] == "captchaID":
				self.captcha_id = attrs[3][1]
				
	def filter_image(self, image):
		""""""
		p = ImageFile.Parser()
		p.feed(self.image_string)
		image = p.close()
		
		image = ImageOps.grayscale(image)
		
		return image
	
class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in URLOpen().open(url).readlines():
				if '<span href="" class="last">' in line:
					name = line.split('<span href="" class="last">')[1].split('</span>')[0]
					if ".." in name:
						tmp = url.split("/").pop().split("_")
						name = ".".join(tmp)
				elif "file uploaded" in line:
					tmp = line.split("file uploaded")[0].split("<span>")[1].split(" ")
					size = int(float(tmp[0]))
					if size == 0:
						size = 1
					unit = tmp[1]
			if not name:
				name = url
				size = -1
		except Exception, e:
			name = url
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	#c = Parser("http://www.filefactory.com/file/cc646e/n/Music_Within_2007_Sample_avi")
	print CheckLinks().check("http://www.filefactory.com/file/cc646e/n/Music_Within_2007_Sample_avi")