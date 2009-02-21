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

SERVICES = ["Megaupload", "Rapidshare", "Gigasize"]

class InputFiles(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_UPLOAD)
		self.set_title(("Input Files"))
		self.set_size_request(600,500)
		
		main_hbox = gtk.HBox()
		self.vbox.pack_start(main_hbox)
		
		package_vbox = gtk.VBox()
		main_hbox.pack_start(package_vbox)

		#package treeview
		frame = gtk.Frame()
		package_vbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.package_treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str))
		scroll.add(self.package_treeview)
		
		self.package_treeview.set_rules_hint(True)
		self.package_treeview.set_headers_visible(False)
		
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.package_treeview.append_column(tree_icon)
				  
		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.package_treeview.append_column(tree_name)
		
		tree_size = gtk.TreeViewColumn('Size') 
		size_cell = gtk.CellRendererText()
		tree_size.pack_start(size_cell, False)
		tree_size.add_attribute(size_cell, 'text', 2)
		self.package_treeview.append_column(tree_size)
		
		#choose path
		hbox = gtk.HBox()
		package_vbox.pack_start(hbox, False, False, 5)
		path_button = gtk.Button(None, gtk.STOCK_OPEN)
		hbox.pack_start(path_button, False, False, 10)
		path_button.set_size_request(90,40)
		path_button.connect("clicked", self.choose_files)
		path_label = gtk.Label(("Choose files to upload."))
		hbox.pack_start(path_label, False, False, 10)
		
		# services treeview
		frame = gtk.Frame()
		main_hbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.services_treeview = gtk.TreeView(gtk.ListStore(gtk.gdk.Pixbuf, str, bool))
		scroll.add(self.services_treeview)
		
		self.services_treeview.set_rules_hint(True)
		self.services_treeview.set_headers_visible(False)
		
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.services_treeview.append_column(tree_icon)
				  
		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.services_treeview.append_column(tree_name)
		
		tree_add = gtk.TreeViewColumn('Add')
		add_cell = gtk.CellRendererToggle()
		#add_cell.connect("toggled", self.toggled)
		tree_add.pack_start(add_cell, True)
		tree_add.add_attribute(add_cell, 'active', 2)
		self.services_treeview.append_column(tree_add)
		
		self.file_icon = self.package_treeview.render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_DND)
		self.correct_icon = self.package_treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		self.incorrect_icon = self.package_treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)

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
		model = self.package_treeview.get_model()
		if os.path.isfile(path):
			if path not in [col[1] for col in model]:
				model.append(None, [self.file_icon, os.path.basename(path), str(os.stat(path).st_size), path])

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = InputFiles()
	#gtk.main()