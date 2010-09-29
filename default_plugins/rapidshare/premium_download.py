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

from premium_cookie import PremiumCookie
from check_links import CheckLinks

from core.service_config import SECTION_PREMIUM_DOWNLOAD
from core.download_plugin import DownloadPlugin
from core.accounts import Accounts
from core.url_open import URLOpen

import core.cons as cons

API_URL = "/cgi-bin/rsapi.cgi"

class FormParser:
	""""""
	def __init__(self, cookie):
		""""""
		self.cookie = cookie
		
	def parse(self, url):
		""""""
		try:
			opener = URLOpen()
			handler = opener.open(url)
			if "text/html" in handler.info()["Content-Type"]:
				cookie_value = self.cookie._cookies[".rapidshare.com"]["/"]["enc"].value
				tmp = url.split("/")
				form =  urllib.urlencode([("sub", "download_v1"), ("cookie", cookie_value), ("fileid", tmp[4]), ("filename", tmp[5])])
				for line in opener.open("http://api.rapidshare.com%s" % API_URL, form).readlines():
					if "DL:" in line:
						url = "http://%s%s" % (line.split("DL:")[1].split(",")[0], API_URL)
						return opener.open(url, form)
			else:
				return opener.open(url)
		except Exception, e:
			logger.error("%s: %s" % (url, e))

class PremiumDownload(DownloadPlugin, Accounts):
	""""""
	def __init__(self, config):
		""""""
		Accounts.__init__(self, config, SECTION_PREMIUM_DOWNLOAD, PremiumCookie())
		DownloadPlugin.__init__(self)

	def check_links(self, url):
		""""""
		return CheckLinks().check(url)

	def add(self, path, link, file_name):
		""""""
		cookie = self.get_cookie()
		if cookie:
			parser = FormParser(cookie)
			return self.start(path, link, file_name, None, None, parser.parse)
			
	def delete(self, file_name):
		""""""
		logger.warning("Stopped %s: %s" % (file_name, self.stop(file_name)))

if __name__ == "__main__":
	c = PremiumCookie()
	p = FormParser(c.get_cookie("",""))
	p.parse("http://rapidshare.com/files/391174483/prueba.bin")
	print URLOpen().open(p.url, p.form).info()