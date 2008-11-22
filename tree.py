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

class Tree(gtk.VBox):
	""""""
	def __init__(self, text):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, int, bool, str, str, str, str, str))
		scroll.add(self.treeview)
		self.pack_start(scroll)

		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		
		#tree columns
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, False)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
				  
		tree_name = gtk.TreeViewColumn('Name')
		tree_name.set_max_width(300)
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, False)
		tree_name.add_attribute(name_cell, 'text', 3)
		self.treeview.append_column(tree_name)
		
		tree_progress = gtk.TreeViewColumn('Progress')
		tree_progress.set_min_width(150)
		progress_cell = gtk.CellRendererProgress()
		tree_progress.pack_start(progress_cell, True)
		tree_progress.add_attribute(progress_cell, 'value', 4)
		tree_progress.add_attribute(progress_cell, 'visible', 5)
		self.treeview.append_column(tree_progress)
		
		tree_current_size = gtk.TreeViewColumn('Current Size')
		current_size_cell = gtk.CellRendererText()
		tree_current_size.pack_start(current_size_cell, False)
		tree_current_size.add_attribute(current_size_cell, 'text', 6)
		self.treeview.append_column(tree_current_size)

		tree_total_size = gtk.TreeViewColumn('Total Size')
		total_size_cell = gtk.CellRendererText()
		tree_total_size.pack_start(total_size_cell, False)
		tree_total_size.add_attribute(total_size_cell, 'text', 7)
		self.treeview.append_column(tree_total_size)
		
		tree_speed = gtk.TreeViewColumn('Speed')
		speed_cell = gtk.CellRendererText()
		tree_speed.pack_start(speed_cell, False)
		tree_speed.add_attribute(speed_cell, 'text', 8)
		self.treeview.append_column(tree_speed)
		
		tree_time = gtk.TreeViewColumn('Time Left')
		time_cell = gtk.CellRendererText()
		tree_time.pack_start(time_cell, False)
		tree_time.add_attribute(time_cell, 'text', 9)
		self.treeview.append_column(tree_time)
		
		tree_plugins = gtk.TreeViewColumn('Plugins')
		plugins_cell = gtk.CellRendererText()
		tree_plugins.pack_start(plugins_cell, False)
		tree_plugins.add_attribute(plugins_cell, 'text', 10)
		self.treeview.append_column(tree_plugins)
		
		#icons
		self.package_icon = self.treeview.render_icon(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)
		self.service_icon = self.treeview.render_icon(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
		self.correct_icon = self.treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		self.failed_icon = self.treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)
		self.active_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
		self.stoped_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_MENU)
		
		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(False)
		self.pack_start(self.status_bar, False)
		self.status_bar.push(self.status_bar.get_context_id(""), "\t" + text)
		
	def add_package(self, dict, name):
		"""TreeStore(icon, status, link, file_name, progress, progress_visible, current_size, total_size, speed, time)"""
		store = self.treeview.get_model()
		str(["anonymousRapidshare", "AnonymousMegaupload"])
		package_iter = store.append(None, [self.package_icon, None, None, name, 0, True, None, None, None, None, None])
		for service, links in dict.items():
			service_iter = store.append(package_iter, [self.service_icon, None, None, service, 0, False, None, None, None, None, None])
			for link in links:
				self.increment_package_size(link[1], link[2], link[3])
				store.append(service_iter, [self.stoped_icon, None, link[0], link[1], 0, True, None, str(link[2])+link[3], None, None, link[4]])
		store.set_value(package_iter, )
		self.treeview.expand_all()


if __name__ == "__main__":
	LINKS = {'rapidshare.com': [('http://rapidshare.com/files/151319465/D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 100, "MB", "AnonymousRapidshare"),
				('http://rapidshare.com/files/151319467/D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 100, "MB", "AnonymousRapidshare"), 
				('http://rapidshare.com/files/151319554/D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 100, "MB", "AnonymousRapidshare"), 
				('http://rapidshare.com/files/151319448/D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 100, "MB", "AnonymousRapidshare"), 
				('http://rapidshare.com/files/151319452/D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 100, "MB", "AnonymousRapidshare"), 
				('http://rapidshare.com/files/151319357/D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 100, "MB", "AnonymousRapidshare")]}
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.maximize()
	t = Tree("mierda")
	window.add(t)
	t.add_package(LINKS, "cojones")
	window.show_all()
	gtk.main()