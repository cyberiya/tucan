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

import pygtk
pygtk.require('2.0')
import gtk
import gobject

class CaptchaDialog(gtk.Dialog):
	""""""
	def __init__(self, service_name, get_captcha, return_solution, parent=None):
		""""""
		gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.set_icon(self.render_icon(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_MENU))
		self.set_title("%s captcha" % service_name)
		self.set_size_request(300,200)
		
		self.get_captcha = get_captcha
		self.return_solution = return_solution
		self.solution = None
		self.timeout = 30

		self.image = gtk.Image()
		self.vbox.pack_start(self.image)

		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 10)
		self.label = gtk.Label("Solve (%i):" % self.timeout)
		hbox.pack_start(self.label, True, True, 5)

		self.entry = gtk.Entry()
		hbox.pack_start(self.entry, False, False, 10)
		self.entry.set_width_chars(24)
		self.entry.set_max_length(40)
		self.entry.set_activates_default(True)
		self.entry.connect("activate", self.solve_captcha)

		button = gtk.Button(None, gtk.STOCK_REFRESH)
		self.action_area.pack_start(button)
		button.connect("clicked", self.new_captcha)
		button = gtk.Button(None, gtk.STOCK_OK)
		self.action_area.pack_start(button)
		button.connect("clicked", self.solve_captcha)

		self.connect("response", self.close)
		
		self.new_captcha()
		gobject.timeout_add(1000, self.check_timeout)
		self.show_all()
		self.run()
			
	def check_timeout(self):
		""""""
		if self.timeout > 0:
			self.timeout -= 1
			self.label.set_text("Solve (%i):" % self.timeout)
			return True
		else:
			self.close()

	def solve_captcha(self, widget=None):
		""""""
		tmp = self.entry.get_text()
		if tmp:
			self.solution = tmp.strip()
		self.close()

	def new_captcha(self, widget=None):
		""""""
		self.timeout = 30
		self.solution = None
		img_type, img_data = self.get_captcha()
		if img_data:
			loader = gtk.gdk.PixbufLoader(img_type)
			loader.write(img_data)
			loader.close()
			self.image.set_from_pixbuf(loader.get_pixbuf())
		else:
			self.image.set_from_pixbuf(self.render_icon(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_DIALOG))
		self.entry.set_text("")
		self.set_focus(self.entry)

	def close(self, widget=None, other=None):
		""""""
		self.return_solution(self.solution)
		self.destroy()

if __name__ == "__main__":
	import urllib2
	def get_captcha():
		content_type = None
		result = None
		f = urllib2.urlopen("http://www.google.com/recaptcha/api/image?c=03AHJ_VuvESiRn8fNqOo1fxuAsK6NRHewDeJ6BWSrX5rD6QpzyL0xOZk9mPlUgkgRDuSx3RjvA81j5gOL8HtZbyUyXAmuyztmWYloQMtJ0azGLs5eAN-8UQdVWg1V3IfXlcwbvKWFb3Rgmfu0A-PuSIcWeVHJLG7lu9Q")
		if "image" in f.info()["Content-Type"]:
			content_type = f.info()["Content-Type"].split("/")[1]
			result = f.read()
		f.close()
		return content_type, result
	def return_solution(solution):
		print solution
	c = CaptchaDialog("Recaptcha!", get_captcha, return_solution)