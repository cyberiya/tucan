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

class Message(gtk.Dialog):
	""""""
	def __init__(self, severity, title, message):
		""""""
		gtk.Dialog.__init__(self)
		self.set_title(title)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_resizable(False)
		self.set_size_request(350,150)
		
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, True, True, 10)
		icon = gtk.STOCK_DIALOG_INFO
		if severity == cons.SEVERITY_WARNING:
			icon = gtk.STOCK_DIALOG_WARNING
		elif severity == cons.SEVERITY_ERROR:
			icon = gtk.STOCK_DIALOG_ERROR
		hbox.pack_start(gtk.image_new_from_stock(icon, gtk.ICON_SIZE_DIALOG), False, False, 30)
		self.set_icon(self.render_icon(icon, gtk.ICON_SIZE_MENU))
		
		label = gtk.Label(message)
		hbox.pack_start(label, True, True)
		label.set_width_chars(40)
		label.set_line_wrap(True) 
		
		#action area
		close_button = gtk.Button(None, gtk.STOCK_CLOSE)
		self.action_area.pack_start(close_button)
		close_button.connect("clicked", self.close)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()

if __name__ == "__main__":
	g = Message(cons.SEVERITY_WARNING, "Not Implemented!", "The Functionality you are trying to use is not implemented yet.")
	gtk.main()