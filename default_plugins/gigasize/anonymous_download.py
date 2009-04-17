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
import cookielib
import logging
logger = logging.getLogger(__name__)

from HTMLParser import HTMLParser

import Image
import ImageOps

from tesseract import Tesseract
from download_plugin import DownloadPlugin
from slots import Slots

from url_open import URLOpen

from check_links import CheckLinks

import cons

WAIT = 60

class FormParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.form_action = None
		self.feed(data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if ((len(attrs) == 3) and (attrs[2][1] == "formDownload")):
				self.form_action = attrs[0][1]
				
class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def __init__(self):
		""""""
		Slots.__init__(self, 1)
		DownloadPlugin.__init__(self)
		
	def check_links(self, url):
		""""""
		return CheckLinks().check(url)

	def add(self, path, link, file_name):
		""""""
		if self.get_slot():
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			opener.open(link)
			form = None
			while not form:
				tes = Tesseract(URLOpen().open("http://www.gigasize.com/randomImage.php").read(), self.filter_image)
				captcha = tes.get_captcha()
				if len(captcha) == 3:
					data = urllib.urlencode({"txtNumber": captcha, "btnLogin.x": "124", "btnLogin.y": "12", "btnLogin": "Download"})
					handle = opener.open("http://www.gigasize.com/formdownload.php", data)
					f = FormParser(handle.read())
					handle.close()
					form = f.form_action
					logger.warning("Captcha: %s" % captcha)
			if self.start(path, "http://www.gigasize.com" + form, file_name, WAIT, cookie, urllib.urlencode({"dlb": "Download"})):
				return True
			else:
				logger.warning("Limit Exceded.")
				self.add_wait()
				
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

	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			logger.warning("Stopped %s: %s" % (file_name, self.return_slot()))
