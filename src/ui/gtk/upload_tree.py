###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
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
import gobject
import pango

import core.cons as cons
import core.misc as misc

import core.cons as cons

STATUS_ICONS = [(cons.STATUS_CORRECT, gtk.STOCK_APPLY), (cons.STATUS_ERROR, gtk.STOCK_CANCEL), (cons.STATUS_WAIT, gtk.STOCK_REFRESH), (cons.STATUS_ACTIVE, gtk.STOCK_MEDIA_PLAY), (cons.STATUS_PEND, gtk.STOCK_MEDIA_PAUSE), (cons.STATUS_STOP, gtk.STOCK_MEDIA_STOP)]

class IconLoader:
	""""""
	def __init__(self, widget):
		""""""
		self.package_icon = widget.render_icon(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
		self.file_icon = widget.render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
		self.link_icons = {}
		for status, stock_icon in STATUS_ICONS:
			self.link_icons[status] = widget.render_icon(stock_icon, gtk.ICON_SIZE_MENU)

	def get_icon(self, item_type, status):
		""""""
		if item_type == cons.ITEM_TYPE_PACKAGE:
			return self.package_icon
		elif item_type == cons.ITEM_TYPE_FILE:
			return self.file_icon
		elif item_type == cons.ITEM_TYPE_LINK:
			return self.link_icons[status]

class UploadTree(gtk.VBox):
	""""""
	def __init__(self, model):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(model)
		scroll.add(self.treeview)
		self.pack_start(scroll)

		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		self.treeview.set_fixed_height_mode(True)

		#tree columns
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, False)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)

		tree_name = gtk.TreeViewColumn('Name')
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width-chars", 60)
		name_cell.set_property("ellipsize", pango.ELLIPSIZE_MIDDLE)
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


"""(icon, status, password, name, progress, progress_visible, current_size, total_size, speed, time, services)"""
