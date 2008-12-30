###############################################################################
##	Tucan Project

##	Copyright (C) 2008 Fran Lupion Crakotak(at)yahoo.es
##	Copyright (C) 2008 Paco Salido beakman(at)riseup.net
##	Copyright (C) 2008 JM Cordero betic0(at)gmail.com

##	This program is free software; you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation; either version 2 of the License, or
##	(at your option) any later version.

##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.

##	You should have received a copy of the GNU General Public License
##	along with this program; if not, write to the Free Software
##	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import urllib
import urllib2
from HTMLParser import HTMLParser

from download_plugin import DownloadPlugin
from slots import Slots

class FormParser(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.form_action = None
		self.url = None
		self.wait = None
		self.feed(urllib2.urlopen(urllib2.Request(url)).read())
		self.close()
		form = {"dl.start": "Free", "":"Free user"}
		self.data = urllib.urlencode(form)
		for line in urllib2.urlopen(self.form_action, self.data).readlines():
			if not self.url:
				self.feed(line)
			else:
				if "var c=" in line:
					self.wait = int(line.split("var c=")[1].split(";")[0])

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if attrs[0][1] == "ff":
				self.form_action = attrs[1][1]
			elif attrs[0][1] == "dlf":
				self.url = attrs[1][1]

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def __init__(self):
		""""""
		Slots.__init__(self, 1)
		DownloadPlugin.__init__(self)
		
	def add(self, path, link, file_name):
		""""""
		if self.get_slot():
			parser = FormParser(link)
			if parser.url:
				return self.start(path, parser.url, file_name, parser.wait)
			else:
				self.add_wait()
				print "Limit Exceded"

	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			print self.return_slot()