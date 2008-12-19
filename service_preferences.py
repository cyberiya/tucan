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

class ServicePreferences(gtk.Dialog):
	""""""
	def __init__(self, name, icon):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon(icon)
		self.set_title(name)
		self.set_size_request(600, 400)
		
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, True, True, 5)
		frame = gtk.Frame()
		hbox.pack_start(frame, False, False, 10)
		store = gtk.TreeStore(str)
		treeview = gtk.TreeView(store)
		frame.add(treeview)
		
		treeview.set_headers_visible(False)
		
		tree_name = gtk.TreeViewColumn('Name')
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width", 100)
		name_cell.set_property("mode", gtk.CELL_RENDERER_MODE_EDITABLE)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 0)
		treeview.append_column(tree_name)
		
		for item in ["Downloads", "Uploads"]:
			iter = store.append(None, [item])
			for subitem in ["Anonymous", "User", "Premium"]:
				store.append(iter, [subitem])
		treeview.expand_all()

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		ok_button = gtk.Button(None, gtk.STOCK_OK)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(ok_button)
		cancel_button.connect("clicked", self.close)
		ok_button.connect("clicked", self.close)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = ServicePreferences("rapidshare.com", gtk.gdk.pixbuf_new_from_file(cons.ICON_MISSING))