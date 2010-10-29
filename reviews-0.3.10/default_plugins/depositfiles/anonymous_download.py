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
logger = logging.getLogger(__name__)

import HTMLParser
import urllib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
from core.slots import Slots

WAIT = 60 #Default, also parsed in the page if possible

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def link_parser(self, url, wait_func, range=None):
		""""""
		try:
			link = None
			opener = URLOpen()
			form =  urllib.urlencode([('gateway_result','1')])
			for line in opener.open(url,form).readlines():
				#Try to get WAIT from the page
				if 'download_waiter_remain' in line:
					try:
						tmp = line.split(">")[2].split("<")[0]
						tmp = int(tmp)
					except ValueError:
						pass
					else:
						if tmp > 0:
							WAIT = tmp
				if 'download_started();' in line:
					link = line.split('action="')[1].split('"')[0]
					break
			if not link:
				return
			if not wait_func(WAIT):
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = URLOpen().open(link, None, range)
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
				if '<div class="info">' in line:
					name = it.next().split('>')[1].split('<')[0].strip()
					tmp = it.next().split('>')[2].split('<')[0].strip()
					unit = tmp[-2:]
					size = int(round(float(tmp[:-2].replace("&nbsp;",""))))
					
					if size > 1024:
						if unit == "KB":
							size = size / 1024
							unit = "MB"
					break
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
