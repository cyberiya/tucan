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

import time
import urllib
import urllib2
import cookielib

from HTMLParser import HTMLParser

from tesseract import Tesseract
from download_plugin import DownloadPlugin
from slots import Slots

import cons

WAIT = 60

class FormParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.form_action = None
		self.feed(data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if ((len(attrs) == 3) and (attrs[2][1] == "formDownload")):
				self.form_action = attrs[0][1]
				print self.form_action
				
	def get_handle(self):
		""""""
		data = urllib.urlencode({"dlb": "Download"})
		print self.form_action
		return urllib2.urlopen(urllib2.Request("http://www.gigasize.com" + self.form_action), data)

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def __init__(self):
		""""""
		Slots.__init__(self, 1)
		DownloadPlugin.__init__(self)
		
	def add(self, path, link, file_name):
		""""""
		if self.get_slot():
			print path, link, file_name
			urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar())))
			urllib2.urlopen(urllib2.Request(link))
			captcha = None
			form = None
			while ((not captcha) and (not form)):
				tes = Tesseract(urllib2.urlopen(urllib2.Request("http://www.gigasize.com/randomImage.php")).read(), True)
				captcha = tes.get_captcha(3)
				data = urllib.urlencode({"txtNumber": captcha, "btnLogin.x": "124", "btnLogin.y": "12", "btnLogin": "Download"})
				handle = urllib2.urlopen(urllib2.Request("http://www.gigasize.com/formdownload.php"), data)
				f = FormParser(handle.read())
				handle.close()
				form = f.form_action
			if self.start(path, link, file_name, WAIT, None, f):
				return True
			else:
				print "Limit Exceded"
				self.add_wait()

	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			print self.return_slot()
