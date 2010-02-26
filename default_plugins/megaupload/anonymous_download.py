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

from check_links import CheckLinks

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
from core.tesseract import Tesseract

import core.cons as cons

WAIT = 45

CAPTCHACODE = "captchacode"
MEGAVAR = "megavar"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func):
		""""""
		link = None
		captcha_img = None
		captchacode = ""
		megavar = ""
		try:
			tmp = url.split("/")
			if len(tmp) > 4:
				del tmp[3]
				url = "/".join(tmp)
			while not link:
				for line in URLOpen().open(url).readlines():
					if "captchacode" in line:
						captchacode = line.split('value="')[1].split('">')[0]
					elif "megavar" in line:
						megavar = line.split('value="')[1].split('">')[0]
					elif "gencap.php" in line:
						captcha_img = line.split('src="')[1].split('"')[0]
				if captcha_img:
					handle = URLOpen().open(captcha_img)
					if handle.info()["Content-Type"] == "image/gif":
						tess = Tesseract(handle.read())
						captcha = tess.get_captcha()
						logger.info("Captcha %s: %s" % (captcha_img, captcha))
						if len(captcha) == 4:
							handle = URLOpen().open(url, urllib.urlencode([(CAPTCHACODE, captchacode), (MEGAVAR, megavar), ("captcha", captcha)]))
							for line in handle.readlines():
								if 'id="downloadlink"' in line:
									link = line.split('<a href="')[1].split('"')[0]
									break
			wait_func(WAIT)
		except Exception, e:
			logger.error(e)
		try:
			handle = URLOpen().open(link)
		except Exception, e:
			self.set_limit_exceeded()
		else:
			return handle

	def check_links(self, url):
		""""""
		return CheckLinks().check(url)
