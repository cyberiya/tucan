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

import logging
logger = logging.getLogger(__name__)

import HTMLParser

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
from core.slots import Slots

WAIT = 40


class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def link_parser(self, url, wait_func, range=None):
		""""""
		try:
			parser = Parser(url)
			if not parser.link:
				return
			elif not wait_func(WAIT):
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = URLOpen().open(parser.link, None, range)
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
			for line in URLOpen().open(url).readlines():
				if '<span id="fileNameTextSpan">' in line:
					name = line.split('<span id="fileNameTextSpan">')[1].split('</span>')[0].strip()
				elif '<td class="finforight' in line:
					size_found += 1
					if size_found == 2:
						tmp = line.split(">")[1].split("<")[0].split()
						unit = tmp[1]
						if "," in tmp[0]:
							size = int(tmp[0].replace(",", ""))
						else:
							size = int(tmp[0])
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

class Parser(HTMLParser.HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.HTMLParser.__init__(self)
		self.tmp_link = None
		self.link = None
		try:
			opener = URLOpen()
			for line in opener.open(url).readlines():
				if "get" in line:
					try:
						self.feed(line)
					except HTMLParser.HTMLParseError, e:
						logger.info("%s :%s %s" % (url, line.strip(), e))
			if self.tmp_link:
				next_line = 0
				for line in opener.open(self.tmp_link).readlines():
					if "id='divDLStart'" in line:
						next_line = 1
					elif next_line:
						next_line = 0
						self.link = line.split("<a href='")[1].split("'")[0]
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ((len(attrs) == 3) and (attrs[1][1] == "dbtn")):
				self.tmp_link = attrs[0][1]
