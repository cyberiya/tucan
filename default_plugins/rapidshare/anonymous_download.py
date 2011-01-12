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

MAX_SIZE = 209796096
API_URL = "/cgi-bin/rsapi.cgi"

class FormParser:
	""""""
	def __init__(self, url):
		""""""
		self.url = None
		self.wait = None
		self.form = None
		try:
			tmp = url.split("/")
			opener = URLOpen()
			form =  urllib.urlencode([("sub", "download_v1"), ("fileid", tmp[4]), ("filename", tmp[5])])
			for line in opener.open("http://api.rapidshare.com%s" % API_URL, form).readlines():
				if "DL:" in line:
					tmp = line.split("DL:")[1].split(",")
					self.url = "http://%s%s" % (tmp[0], API_URL)
					self.form =  "%s&%s" % (form, urllib.urlencode([("dlauth", tmp[1])]))
					self.wait = int(tmp[2])
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
			
	def get_handler(self, url):
		""""""
		if self.form:
			return URLOpen().open(self.url, self.form)

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def __init__(self):
		""""""
		Slots.__init__(self, 1)
		DownloadPlugin.__init__(self)

	def check_links(self, url):
		""""""
		return CheckLinks().check(url, MAX_SIZE)

	def add(self, path, link, file_name):
		""""""
		if self.get_slot():
			parser = FormParser(link)
			if parser.url:
				return self.start(path, parser.url, file_name, parser.wait, None, parser.get_handler)
			else:
				self.add_wait()
				self.return_slot()
				logger.warning("Limit Exceeded.")

	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			logger.warning("Stopped %s: %s" % (file_name, self.return_slot()))

if __name__ == "__main__":
	p = FormParser("http://rapidshare.com/files/391174483/prueba.bin")
	print p.url, p.form, p.wait
