###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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

import logging
import cookielib
logger = logging.getLogger(__name__)

import urllib

import Image
import ImageOps

from core.tesseract import Tesseract
from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
import core.cons as cons

import time

WAIT = 60 #Default, also parsed in the page if possible
BASE_URL = "http://www.gigasize.com"


class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			captcha_url = None
			wait = WAIT
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			if not wait_func():
				return
			opener.open(url)
			retry = 5
			while retry:
				tes = Tesseract(opener.open("http://www.gigasize.com/randomImage.php").read(), self.filter_image)
				captcha = tes.get_captcha()
				if len(captcha) == 3:
					logger.warning("Captcha: %s" % captcha)
					data = urllib.urlencode([("txtNumber", captcha)])
					it = opener.open("http://www.gigasize.com/formdownload.php", data)
					for line in it:
						if '<div id="askPws" style="display:block">' in line:
							return self.set_limit_exceeded()
						if "formDownload" in line:
							action = line.split('action="')[1].split('"')[0]
							it.next()
							it.next()
							wait = int(it.next().split('>')[1].split('<')[0])
							if not wait_func(wait):
								return
							return opener.open("%s%s" % (BASE_URL,action))
				retry -= 1
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = URLOpen().open(url)
			for line in it:
				if "<p><strong>Name</strong>" in line:
					name = line.split("<b>")[1].split("</b>")[0].strip()
				elif "<p>Size:" in line:
					tmp = line.split("<span>")[1].split("</span>")[0].strip()
					if cons.UNIT_KB in tmp:
						unit = cons.UNIT_KB
						size = int(float(tmp.split(cons.UNIT_KB)[0]))
					elif cons.UNIT_MB in tmp:
						unit = cons.UNIT_MB
						size = int(float(tmp.split(cons.UNIT_MB)[0]))
					elif cons.UNIT_GB in tmp:
						unit = cons.UNIT_GB
						size = int(float(tmp.split(cons.UNIT_GB)[0]))
			if "get.php?d=" not in url:
				name = url.split("/").pop()
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
		
	def filter_image(self, image):
		""""""
		image = image.resize((120,40), Image.BICUBIC)
		image = image.crop((30,9,86,32))
		image = image.point(self.filter_pixel)
		image = ImageOps.grayscale(image)
		return image

	def filter_pixel(self, pixel):
		""""""
		if pixel > 60:
			return 255
		else:
			return 1
