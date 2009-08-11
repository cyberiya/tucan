###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crak@tucaneando.com
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

from file_chooser import FileChooser

import cons

class AdvancedPackages(gtk.Dialog):
	""""""
	def __init__(self, default_path, packages):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_PACKAGE)
		self.set_title(_("Advanced Packages"))
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(600,400)

		self.packages = []
		self.history_path = default_path

		#treeview
		frame = gtk.Frame()
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(gtk.ListStore(gtk.gdk.Pixbuf, str, str, str))
		scroll.add(self.treeview)

		self.treeview.set_rules_hint(True)
		#self.treeview.set_headers_visible(False)

		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)

		tree_path = gtk.TreeViewColumn('Path') 
		path_cell = gtk.CellRendererText()
		tree_path.pack_start(path_cell, True)
		tree_path.add_attribute(path_cell, 'text', 1)
		self.treeview.append_column(tree_path)
		self.treeview.connect("row-activated", self.choose)

		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		name_cell.set_property("editable", True)
		name_cell.connect("edited", self.change, 2)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 2)
		self.treeview.append_column(tree_name)

		tree_pass = gtk.TreeViewColumn('Password') 
		pass_cell = gtk.CellRendererText()
		pass_cell.set_property("editable", True)
		pass_cell.connect("edited", self.change, 3)
		tree_pass.pack_start(pass_cell, True)
		tree_pass.add_attribute(pass_cell, 'text', 3)
		self.treeview.append_column(tree_pass)

		#fill treestore
		package_icon = gtk.gdk.pixbuf_new_from_file(cons.ICON_PACKAGE)
		model = self.treeview.get_model()
		for package_name, package_links in packages:
			model.append((package_icon, default_path, package_name, None))

		#choose path
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 5)
		path_button = gtk.Button(None, gtk.STOCK_OPEN)
		hbox.pack_start(path_button, False, False, 10)
		path_button.set_size_request(90,40)
		path_button.connect("clicked", self.choose_path)
		path_label = gtk.Label(_("Choose new path for selected Package."))
		hbox.pack_start(path_label, False, False, 10)

		#action area
		ok_button = gtk.Button(None, gtk.STOCK_OK)
		self.action_area.pack_start(ok_button)
		ok_button.connect("clicked", self.configure_packages)

		self.connect("response", self.close)
		self.show_all()
		self.run()

	def configure_packages(self, button=None):
		""""""
		model = self.treeview.get_model()
		for package in model:
			self.packages.append((package[1], package[2], package[3]))
		self.close()

	def choose(self, treeview, path, view_column):
		""""""
		self.choose_path()

	def choose_path(self, button=None):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			f = FileChooser(self, self.on_choose, self.history_path)
			self.history_path = f.history_path

	def on_choose(self, folder_path):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			model.set_value(iter, 1, folder_path)

	def change(self, cellrenderertext, path, new_text, column):
		""""""
		model = self.treeview.get_model()
		model.set_value(model.get_iter(path), column, new_text)

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
