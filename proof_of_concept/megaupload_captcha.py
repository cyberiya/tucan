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
import time
import socket

from megaupload_parsers import CaptchaParser
from megaupload_parsers import UrlParser
from tesseract import Tesseract

BUFFER_SIZE = 1024

URL = ""

class Captcha:
	""""""
	def __init__(self, url):
		""""""
		self.url = url
		self.link = None
		cont = 0
		while not self.link and cont < 10:
			self.get_link()
			cont += 1
		print self.link

	def get_link(self):
		""""""
		c_parser = CaptchaParser(self.url)
		handle = urllib2.urlopen(urllib2.Request(c_parser.form_action + c_parser.captcha))
		tes = Tesseract(handle.read())
		handle.close()
		self.captcha = tes.get_captcha(3)
		if self.captcha:
			form = {"d": c_parser.form_d, "imagecode": c_parser.form_imagecode, "megavar": c_parser.form_megavar, "imagestring" : self.captcha.strip()}
			data = urllib.urlencode(form)
			handle = urllib2.urlopen(c_parser.form_action, data)
			u_parser = UrlParser(handle.read())
			handle.close()
			if  u_parser.tmp_url:
				self.link = u_parser.get_url()

if __name__ == "__main__":

	socket.setdefaulttimeout(15)

	c = Captcha(URL)
	time.sleep(45)
	if c.link:
		print c.link.split("/").pop()
		f = file(c.link.split("/").pop() , "w")
		handle = urllib2.urlopen(c.link)
		
		elapsed = time.time()
		
		data = handle.read(BUFFER_SIZE)
		f.write(data)
				
		while len(data) > 0:
			try:
				data = handle.read(BUFFER_SIZE)
				f.write(data)
			except socket.timeout:
				print "timed out"
				break
		print int((time.time() - elapsed)/60), "minutos"
		f.close()