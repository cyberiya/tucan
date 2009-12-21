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
import logging
logger = logging.getLogger(__name__)

from premium_cookie import PremiumCookie
from check_links import CheckLinks

from core.service_config import SECTION_PREMIUM_DOWNLOAD
from core.download_plugin import DownloadPlugin
from core.accounts import Accounts
from core.url_open import URLOpen

import core.cons as cons

class FormParser:
	""""""
	def __init__(self, url, cookie):
		""""""
		self.url = None
		try:
			opener = URLOpen(cookie)
			handler = opener.open(url)
			if "text/html" in handler.info()["Content-Type"]:
				for line in handler.readlines():
					if '<form id="ff"' in line:
						form_action = line.split('action="')[1].split('" method="post">')[0]
						for line in opener.open(form_action, urllib.urlencode({"dl.start": "PREMIUM", "":"Premium user"})).readlines():
							if '<form name="dlf"' in line:
								self.url = line.split('name="dlf" action="')[1].split('" method="post"')[0]
						break
			else:
				self.url = url
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
			f = FormParser(link, cookie)
			if f.url:
				return self.start(path, f.url, file_name, None, cookie)

	def delete(self, file_name):
		""""""
		logger.warning("Stopped %s: %s" % (file_name, self.stop(file_name)))

if __name__ == "__main__":
	c = PremiumCookie()
	p = FormParser("http://rapidshare.com/files/28374629/30_-_Buscate_la_Vida_-_Novia_2000_by_shagazz.part2.rar", c.get_cookie("",""))
	print p.url