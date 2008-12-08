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
	def __init__(self, get_files):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, int, bool, str, str, str, str, str))
		scroll.add(self.treeview)
		self.pack_start(scroll)

		self.get_files = get_files

		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		
		#tree columns
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, False)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
				  
		tree_name = gtk.TreeViewColumn('Name')
		tree_name.set_max_width(350)
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
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
		self.package_icon = self.treeview.render_icon(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
		self.active_service_icon = self.treeview.render_icon(gtk.STOCK_YES, gtk.ICON_SIZE_MENU)
		self.unactive_service_icon = self.treeview.render_icon(gtk.STOCK_NO, gtk.ICON_SIZE_MENU)
		self.correct_icon = self.treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		self.failed_icon = self.treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)
		self.wait_icon = self.treeview.render_icon(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
		self.active_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
		self.pending_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU)
		self.stoped_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_MENU)
		self.icons = {cons.STATUS_CORRECT: self.correct_icon, cons.STATUS_ERROR: self.failed_icon, cons.STATUS_WAIT: self.wait_icon, cons.STATUS_ACTIVE: self.active_icon, cons.STATUS_PEND: self.pending_icon, cons.STATUS_STOP: self.stoped_icon}
		
		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(False)
		self.pack_start(self.status_bar, False)
		self.status_bar.push(self.status_bar.get_context_id(""), "\t" + "No Downloads Active.")
		self.updating = False

	def add_package(self, package_name, package_path, package):
		"""
		TreeStore(icon, status, path, name, progress, progress_visible, current_size, total_size, speed, time, services)
		"""
		package_size = 0
		package_unit = cons.UNIT_KB
		model = self.treeview.get_model()
		package_iter = model.append(None, [self.package_icon, cons.STATUS_PEND, None, package_name, 0, True, None, None, None, None, package_path])
		for item in package:
			package_size += item[3]
			package_unit = item[4]
			item_iter = model.append(package_iter, [self.pending_icon, cons.STATUS_PEND, None, item[1], 0, True, None, str(item[3])+item[4], None, None, str(item[2])])
			self.treeview.expand_to_path(model.get_path(item_iter))
			for link in item[0]:
				link_iter = model.append(item_iter, [self.unactive_service_icon, cons.STATUS_PEND, None, link, 0, False, None, None, None, None, item[5][item[0].index(link)]])
		model.set_value(package_iter, 7, str(package_size)+package_unit)
		if not self.updating:
			self.updating = True
			gobject.timeout_add(1000, self.update)
		return package_iter
		
	def update(self):
		"""(icon, status, path, name, progress, progress_visible, current_size, total_size, speed, time, services)"""
		files = self.get_files()
		if len(files) > 0:
			model = self.treeview.get_model()
			package_iter = model.get_iter_root()
			while package_iter:
				file_iter = model.iter_children(package_iter)
				#package_status = model.set_value(package_iter, 0)
				package_progress = 0
				package_actual_size = 0
				package_unit = cons.UNIT_KB
				package_speed = 0
				while file_iter:
					name = model.get_value(file_iter, 3)
					for file in files:
						if file.name == name:
							model.set_value(file_iter, 0, self.icons[file.status])
							model.set_value(file_iter, 1, file.status)
							model.set_value(file_iter, 4, file.progress)
							package_progress += file.progress
							if file.actual_size > 0:
								model.set_value(file_iter, 6, str(file.actual_size)+file.size_unit)
								package_actual_size += file.actual_size
							model.set_value(file_iter, 7, str(file.total_size)+file.size_unit)
							package_unit = file.size_unit
							if file.speed > 1:
								model.set_value(file_iter, 8, str(file.speed)+cons.UNIT_SPEED)
								package_speed += file.speed
							elif file.speed == 0:
								model.set_value(file_iter, 8, None)
							if file.status == cons.STATUS_CORRECT:
								if not file.time > 0:
									file.time = 1
							model.set_value(file_iter, 9, self.calculate_time(file.time))
							link_iter = model.iter_children(file_iter)
							while link_iter:
								for tmp_link in file.links:
									if tmp_link.url == model.get_value(link_iter, 3):
										service_icon = self.unactive_service_icon
										if tmp_link.active:
											service_icon = self.active_service_icon
										model.set_value(link_iter, 0, service_icon)
								link_iter = model.iter_next(link_iter)
								
					model.set_value(package_iter, 4, int(package_progress/model.iter_n_children(package_iter)))
					if package_actual_size > 0:
						model.set_value(package_iter, 6, str(package_actual_size)+package_unit)
					if package_speed > 0:
						model.set_value(package_iter, 8, str(package_speed)+cons.UNIT_SPEED)
					else:
						model.set_value(package_iter, 8, None)
					file_iter = model.iter_next(file_iter)
				package_iter = model.iter_next(package_iter)
		return True

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
		elif seconds > 0:
			result = str(seconds) + "s"
		return result
