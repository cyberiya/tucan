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
from core.slots import Slots

#MAX_SIZE = 209796096
MAX_SIZE = None

API_URL = "/cgi-bin/rsapi.cgi"

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		link = None
		wait = 0
		try:
			tmp = url.split("/")
			opener = URLOpen()
			form =  urllib.urlencode([("sub", "download_v1"), ("fileid", tmp[4]), ("filename", tmp[5])])
			for line in opener.open("http://api.rapidshare.com%s" % API_URL, form, content_range):
				if "DL:" in line:
					tmp = line.split("DL:")[1].split(",")
					link = "http://%s%s" % (tmp[0], API_URL)
					form =  "%s&%s" % (form, urllib.urlencode([("dlauth", tmp[1])]))
					wait = int(tmp[2])
			if not wait_func(wait):
				return
			elif link:
				return URLOpen().open(link, form, content_range)
			else:
				return self.set_limit_exceeded()
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		return CheckLinks().check(url, MAX_SIZE)
