###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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

import logging
logger = logging.getLogger(__name__)

import HTMLParser
import urllib
import cookielib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
from core.slots import Slots

WAIT = 50

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def link_parser(self, url, wait_func, range=None):
		""""""
		try:
			self.link = None
			self.cookie = cookielib.CookieJar()
			self.opener = URLOpen(self.cookie)
			try:
				form = urllib.urlencode([("referer2", ""), ("download", 1), ("imageField.x", 81), ("imageField.y", 29)])
				for line in self.opener.open(url,form).readlines():
					if 'link_enc=new Array' in line:
						tmp = line.strip().split("var link_enc=new Array(")[1].split(");")[0]
						tmp = eval("[%s]" % tmp)
						self.link = "".join(tmp)
						break
			except Exception, e:
				logger.exception("%s :%s" % (url, e))
				
			if not self.link:
				return
			if not wait_func(WAIT):
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = self.opener.open(self.link, None, range)
			except Exception, e:
				self.set_limit_exceeded()
			else:
				return handle

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		size_found = 0
		try:
			it = iter(URLOpen().open(url).readlines())
			for line in it:
				if 'File Name:' in line:
					name = it.next().split('>')[1].split('<')[0]
				if 'File Size:' in line:
					tmp = line.split('>')[3].split('<')[0]
					if "KB" in tmp:
						size = int(round(float(tmp.split("KB")[0])))
						unit = "KB"
					elif "MB" in tmp:
						size = float(tmp.split("MB")[0])
						if int(round(size)) > 0:
							size = int(round(size))
							unit = "MB"
						else:
							size = int(round(1024 * size))
							unit = "KB"
					elif "GB" in tmp:
						size = int(round(float(tmp.split("GB")[0])))
						unit = "GB"
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
