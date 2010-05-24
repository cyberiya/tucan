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

from core.accounts import Accounts
from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

class PremiumDownload(DownloadPlugin, Accounts):
	""""""
	def __init__(self, config, section):
		""""""
		Accounts.__init__(self, config, section, PremiumCookie())
		DownloadPlugin.__init__(self, config, section)

	def link_parser(self, url, wait_func, range=None):
		""""""
		try:
			cookie = self.get_cookie()
			if not wait_func():
				return
			opener = URLOpen(cookie)
			handler = opener.open(url, None, range)
			if not wait_func():
				return
			if "text/html" in handler.info()["Content-Type"]:
				for line in handler.readlines():
					if '<form id="ff"' in line:
						form_action = line.split('action="')[1].split('" method="post">')[0]
						for line in opener.open(form_action, urllib.urlencode({"dl.start": "PREMIUM", "":"Premium user"})).readlines():
							if '<form name="dlf"' in line:
								return opener.open(line.split('name="dlf" action="')[1].split('" method="post"')[0], None, range)
						break
			else:
				return handler
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		return CheckLinks().check(url)
