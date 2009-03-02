###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crakotaku(at)yahoo.es
## Copyright (C) 2008-2009 Paco Salido beakman(at)riseup.net
## Copyright (C) 2008-2009 JM Cordero betic0(at)gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
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

import pygtk
pygtk.require('2.0')
import gtk

import urllib
import urllib2

URL = "http://www.megaupload.com/es/?d=RDAJ2PYH"
QUERY = "http://localhost:8080/query"
ADD = "http://localhost:8080/add"

class CaptchaParser(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_size_request(300,200)
		
		self.image = gtk.Image()
		self.vbox.pack_start(self.image)
		
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 10)
		self.label = gtk.Label()
		hbox.pack_start(self.label)
		
		self.entry = gtk.Entry()
		hbox.pack_start(self.entry, False, False, 10)
		self.entry.set_width_chars(5)
		self.entry.set_max_length(4)
		self.entry.set_activates_default(True)
		self.entry.connect("activate", self.new_captcha)
		
		self.captcha = None
		self.new_captcha()
		
		button = gtk.Button(None, gtk.STOCK_REFRESH)
		self.action_area.pack_start(button)
		button.connect("clicked", self.new_captcha)
		button = gtk.Button(None, gtk.STOCK_ADD)
		self.action_area.pack_start(button)
		#button.connect("clicked", self.store_captcha)

		self.connect("response", self.close)
		self.show_all()
		self.run()
	
	def new_captcha(self, widget=None):
		""""""
		captcha = None
		for line in urllib2.urlopen(urllib2.Request(URL)).readlines():
			if "gencap.php?" in line:
				captcha = line.split('<img src="')[1].split('" border="0"')[0]
		if captcha:
			loader = gtk.gdk.PixbufLoader("gif")
			loader.write(urllib2.urlopen(urllib2.Request(captcha)).read())
			loader.close()
			self.image.set_from_pixbuf(loader.get_pixbuf())
			self.entry.set_text("")
			self.set_focus(self.entry)
			self.label.set_text("Solve Captcha: %s" % captcha.split("gencap.php?")[1].split(".gif")[0])
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()

	def query_captcha(self, captcha):
		""""""
		response = urllib2.urlopen(urllib2.Request(QUERY), urllib.urlencode([("key", captcha)])).read()
		if len(response) > 0:
			return response.split(",")

	def add_captcha(self, captcha, solution):
		""""""
		data = urllib.urlencode([("key", captcha), ("value", solution)])
		response = urllib2.urlopen(urllib2.Request(ADD), data).read()
		if len(response) > 0:
			return True

if __name__ == "__main__":
	c = CaptchaParser()
