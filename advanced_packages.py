###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion Crakotak(at)yahoo.es
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

import cons

PACKAGES = [('D.S03E06.LOL.cHoPPaHoLiK.part', [(['http://www.megaupload.com/?d=UE8EQ0JZ', 'http://rapidshare.com/files/160153330/D.S03E06.LOL.cHoPPaHoLiK.part1.rar'], 'D.S03E06.LOL.cHoPPaHoLiK.part1.rar', ['megaupload.com', 'rapidshare.com'], 200, 'MB', ['AnonymousMegaupload', 'AnonymousRapidshare']), (['http://www.megaupload.com/?d=2MCQZBP4', 'http://rapidshare.com/files/160153273/D.S03E06.LOL.cHoPPaHoLiK.part2.rar'], 'D.S03E06.LOL.cHoPPaHoLiK.part2.rar', ['megaupload.com', 'rapidshare.com'], 200, 'MB', ['AnonymousMegaupload', 'AnonymousRapidshare']), (['http://www.megaupload.com/?d=QNVY9GXH', 'http://rapidshare.com/files/160153250/D.S03E06.LOL.cHoPPaHoLiK.part3.rar'], 'D.S03E06.LOL.cHoPPaHoLiK.part3.rar', ['megaupload.com', 'rapidshare.com'], 150, 'MB', ['AnonymousMegaupload', 'AnonymousRapidshare'])]), ('D.S03E07.LOL.cHoPPaHoLiK.part', [(['http://www.megaupload.com/?d=0UGD9XIW', 'http://rapidshare.com/files/169034268/D.S03E07.LOL.cHoPPaHoLiK.part1.rar'], 'D.S03E07.LOL.cHoPPaHoLiK.part1.rar', ['megaupload.com', 'rapidshare.com'], 191, 'MB', ['AnonymousMegaupload', 'AnonymousRapidshare']), (['http://www.megaupload.com/?d=AGF6MW15', 'http://rapidshare.com/files/169034282/D.S03E07.LOL.cHoPPaHoLiK.part2.rar'], 'D.S03E07.LOL.cHoPPaHoLiK.part2.rar', ['megaupload.com', 'rapidshare.com'], 191, 'MB', ['AnonymousMegaupload', 'AnonymousRapidshare']), (['http://www.megaupload.com/?d=3IWUNAJT', 'http://rapidshare.com/files/169034298/D.S03E07.LOL.cHoPPaHoLiK.part3.rar'], 'D.S03E07.LOL.cHoPPaHoLiK.part3.rar', ['megaupload.com', 'rapidshare.com'], 169, 'MB', ['AnonymousMegaupload', 'AnonymousRapidshare'])])]
PATH = "/home/crak/downloads/"

class AdvancedPackages(gtk.Dialog):
	""""""
	def __init__(self, default_path, packages):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_PACKAGE)
		self.set_title("Advanced Packages")
		self.set_size_request(600,400)
		
		self.packages = []
		
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
		path_label = gtk.Label("Choose new path for selected Package.")
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
	
	def choose_path(self, button):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			self.filechooser = gtk.FileChooserDialog('Select a Folder', self, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
			choose_button = gtk.Button(None, gtk.STOCK_OK)
			self.filechooser.action_area.pack_start(choose_button)
			self.filechooser.connect("response", self.on_choose, model.get_path(iter))
			choose_button.connect("clicked", self.on_choose, None, model.get_path(iter))
			self.filechooser.set_position(gtk.WIN_POS_CENTER)
			self.filechooser.show_all()
			self.filechooser.run()
			
	def on_choose(self, widget, other, path):
		""""""
		self.change(None, path, self.filechooser.get_filename() + "/", 1)
		self.filechooser.destroy()
		del self.filechooser

	def change(self, cellrenderertext, path, new_text, column):
		""""""
		model = self.treeview.get_model()
		model.set_value(model.get_iter(path), column, new_text)

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = AdvancedPackages(PATH, PACKAGES)
	gtk.main()