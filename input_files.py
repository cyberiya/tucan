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

import os

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from file_chooser import FileChooser

import cons

class InputFiles(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_UPLOAD)
		self.set_title(("Input Files"))
		self.set_size_request(600,500)

		#choose path
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 5)
		path_button = gtk.Button(None, gtk.STOCK_OPEN)
		hbox.pack_start(path_button, False, False, 10)
		path_button.set_size_request(90,40)
		path_button.connect("clicked", self.choose_files)
		path_label = gtk.Label(("Choose files to upload."))
		hbox.pack_start(path_label, False, False, 10)

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		add_button = gtk.Button(None, gtk.STOCK_ADD)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(add_button)
		cancel_button.connect("clicked", self.close)
		#add_button.connect("clicked", self.choose_files)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def choose_files(self, button):
		""""""
		FileChooser(self, self.on_choose, None, True)
		
	def on_choose(self, path):
		""""""
		#comprobar si es un directorio
		print path, os.stat(path).st_size

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = InputFiles()
	#gtk.main()