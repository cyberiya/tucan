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

class FormParser:
	""""""
	def __init__(self, url):
		""""""
		self.url = None
		self.wait = None
		try:
			for line in URLOpen().open(url).readlines():
				if '<form id="ff"' in line:
					form_action = line.split('action="')[1].split('" method="post">')[0]
					self.data = urllib.urlencode({"dl.start": "Free", "":"Free user"})
					for line in URLOpen().open(form_action, self.data).readlines():
						if "var tt =" in line:
							self.url = line.split('name="dlf" action="')[1].split('" method="post"')[0]
						elif "var c=" in line:
							self.wait = int(line.split("var c=")[1].split(";")[0])
					break
		except Exception, e:
			print e
			logger.exception("%s: %s" % (url, e))

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
			parser = FormParser(link)
			if parser.url:
				return self.start(path, parser.url, file_name, parser.wait)
			else:
				self.add_wait()
				self.return_slot()
				logger.warning("Limit Exceeded.")

	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			logger.warning("Stopped %s: %s" % (file_name, self.return_slot()))

if __name__ == "__main__":
	p = FormParser("http://rapidshare.com/files/28374629/30_-_Buscate_la_Vida_-_Novia_2000_by_shagazz.part2.rar")
	print p.url
