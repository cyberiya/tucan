#####################################################################################
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
#####################################################################################

import urllib
import urllib2

from HTMLParser import HTMLParser

BUFFER_SIZE = 1024

URL = ""

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
		handle = urllib2.urlopen(self.form_action, self.data)
		self.download_data = handle.read()
		for line in self.download_data.split("\n"):
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


if __name__ == "__main__":
	c = FormParser(URL)
	if c.wait:
		print c.wait
		time.sleep(c.wait)
		print c.url.split("/").pop()
		f = file(c.url.split("/").pop() , "w")
		handle = urllib2.urlopen(c.url)
		data = handle.read(BUFFER_SIZE)
		f.write(data)
		while len(data) > 0:
			data = handle.read(BUFFER_SIZE)
			f.write(data)
		f.close()
	else:
		print "espera 5 minutos"
