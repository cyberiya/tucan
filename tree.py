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
import gobject

import cons

class Tree(gtk.VBox):
	""""""
	def __init__(self, get_plugin, text):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, int, bool, str, str, str, str, str))
		scroll.add(self.treeview)
		self.pack_start(scroll)

		self.get_plugin = get_plugin

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
		
		tree_plugins = gtk.TreeViewColumn('Plugin')
		plugins_cell = gtk.CellRendererText()
		tree_plugins.pack_start(plugins_cell, False)
		tree_plugins.add_attribute(plugins_cell, 'text', 10)
		self.treeview.append_column(tree_plugins)
		
		#icons
		self.package_icon = self.treeview.render_icon(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)
		self.service_icon = self.treeview.render_icon(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
		self.correct_icon = self.treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		self.failed_icon = self.treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)
		self.wait_icon = self.treeview.render_icon(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
		self.active_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
		self.pending_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU)
		self.stoped_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_MENU)
		
		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(False)
		self.pack_start(self.status_bar, False)
		self.status_bar.push(self.status_bar.get_context_id(""), "\t" + text)
		self.add_package({'rapidshare.com': [('http://rapidshare.com/files/151319465/D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 100, 'MB', 'AnonymousRapidshare'), ('http://rapidshare.com/files/151319467/D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 100, 'MB', 'AnonymousRapidshare'), ('http://rapidshare.com/files/151319554/D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 100, 'MB', 'AnonymousRapidshare'), ('http://rapidshare.com/files/151319448/D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 100, 'MB', 'AnonymousRapidshare'), ('http://rapidshare.com/files/151319452/D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 100, 'MB', 'AnonymousRapidshare'), ('http://rapidshare.com/files/151319357/D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 100, 'MB', 'AnonymousRapidshare')]}, "D.S03E02.0TV.cHoPPaHoLiK")
		
	def add_package(self, dict, name):
		"""TreeStore(icon, status, link/path, file_name, progress, progress_visible, current_size, total_size, speed, time, plugin/services)"""
		package_size = PackageValue()
		store = self.treeview.get_model()
		package_iter = store.append(None, [self.package_icon, cons.STATUS_PEND, "/home/crak/downloads/", name, 0, True, None, None, None, None, str(dict.keys())])
		for service, links in dict.items():
			service_iter = store.append(package_iter, [self.service_icon, cons.STATUS_PEND, None, service, 0, False, None, None, None, None, None])
			for link in links:
				package_size.update(link[1], link[2], link[3])
				store.append(service_iter, [self.pending_icon, cons.STATUS_PEND, link[0], link[1], 0, True, None, str(link[2])+link[3], None, None, link[4]])
		store.set_value(package_iter, 7, package_size.get())
		self.treeview.expand_all()
		
	def start_item(self, iter):
		""""""
		model = self.treeview.get_model()
		if not model.iter_has_child(iter):
			link = model.get_value(iter, 2)
			name = model.get_value(iter, 3)
			plugin_name = model.get_value(iter, 10)
			if self.get_plugin(None, plugin_name)[1].add_download(link, name):
				gobject.timeout_add(2000, self.update, iter)
				return True
	
	def stop_item(self, iter):
		""""""
		model = self.treeview.get_model()
		if not model.iter_has_child(iter):
			name = model.get_value(iter, 3)
			plugin_name = model.get_value(iter, 10)
			if self.get_plugin(None, plugin_name)[1].stop_download(name):
				return True
		
	def update(self, iter):
		""""""
		result = True
		model = self.treeview.get_model()
		link = model.get_value(iter, 2)
		name = model.get_value(iter, 3)
		plugin_name = model.get_value(iter, 10)
		status, progress, size, unit, speed, time = self.get_plugin(None, plugin_name)[1].get_status(name)
		print status, progress, size, unit, speed, time
		icon = self.pending_icon
		if status == cons.STATUS_WAIT:
			icon = self.wait_icon
			size = None
			speed = None
			time = str(time) + " seconds"
		elif status == cons.STATUS_ACTIVE:
			icon = self.active_icon
			size = str(size)+unit
			time = self.calculate_time(time)
		elif status == cons.STATUS_STOP:
			icon = self.stoped_icon
			progress = 0
			time = None
			size = None
			speed = None
			result = False
		elif status == cons.STATUS_CORRECT:
			icon = self.correct_icon
			progress = 100
			size = str(size)+unit
			time = self.calculate_time(time)
			speed = None
			result = False
		else:
			icon = self.failed_icon
			progress = 0
			time = None
			size = None
			speed = None
			result = False
		model.set(iter, 0, icon, 1, status, 4, progress, 6, size, 8, speed, 9, time)
		return result
		
	def calculate_time(self, time):
		""""""
		result = None
		hours = 0
		minutes = 0
		while time >= cons.HOUR:
			time = time - cons.HOUR
			hours += 1
		while time >= cons.MINUTE:
			time = time - cons.MINUTE
			minutes += 1
		seconds = time
		if hours > 0:
			result = str(hours) + "h" + str(minutes) + "m" + str(seconds) + "s"
		elif minutes > 0:
			result =  str(minutes) + "m" + str(seconds) + "s"
		else:
			result = str(seconds) + "s"
		return result
		
class PackageValue:
	""""""
	def __init__(self):
		""""""
		self.links = []
		self.value = 0
		self.value_unit = None
		
	def update(self, name, value, unit):
		""""""
		if not name in self.links:
			self.links.append(name)
			self.value += value
			self.value_unit = unit
		
	def get(self):
		""""""
		return str(self.value) + self.value_unit