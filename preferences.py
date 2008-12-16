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

import pygtk
pygtk.require('2.0')
import gtk

import cons

class Preferences(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon(self.render_icon(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU))
		self.set_title("Preferences")
		self.set_size_request(500,500)
		
		notebook = gtk.Notebook()
		self.vbox.pack_start(notebook)
		for item in [cons.ICON_PREFERENCES_MAIN, cons.ICON_PREFERENCES_PLUGINS, cons.ICON_PREFERENCES_ADVANCED]:
			vbox = gtk.VBox()
			vbox.set_size_request(100, -1)
			vbox.pack_start(gtk.image_new_from_file(item))
			vbox.pack_start(gtk.Label(item))
			vbox.show_all()
			notebook.append_page(gtk.VBox(), vbox)

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		save_button = gtk.Button(None, gtk.STOCK_SAVE)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(save_button)
		cancel_button.connect("clicked", self.close)
		save_button.connect("clicked", self.close)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = Preferences()