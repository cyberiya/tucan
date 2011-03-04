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

from queue_model import QueueModel

from core.upload_manager import UploadManager

import core.cons as cons
import core.misc as misc

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

class UploadTree(gtk.VBox, UploadManager):
	""""""
	def __init__(self):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.pack_start(scroll)

		model = QueueModel(IconLoader(self))
		UploadManager.__init__(self, model)
		self.treeview = gtk.TreeView(model)
		scroll.add(self.treeview)

		self.treeview.set_rules_hint(True)
		#self.treeview.set_headers_visible(False)
		#self.treeview.set_fixed_height_mode(True)

		COLUMNS = (
		("Status", "pixbuf", 0, []),
		("Name", "text", 1, [("width-chars", 40), ("ellipsize", pango.ELLIPSIZE_MIDDLE)]),
		("Progress", "value", 2, [("width", 150)]),
		("Current Size", "text", 3, []),
		("Total Size", "text", 4, []),
		("Speed", "text", 5, []),
		("ETA", "text", 6, []),
		("Info", "text", 7, [])
		)

		for name, attr, value, properties in COLUMNS:
			column = gtk.TreeViewColumn(name)
			#column.set_property("fixed-width", width)
			#column.set_resizable(True)
			if attr == "pixbuf":
				cell = gtk.CellRendererPixbuf()
			elif attr == "value":
				cell = gtk.CellRendererProgress()
			elif attr == "text":
				cell = gtk.CellRendererText()
			for property, pvalue in properties:
				cell.set_property(property, pvalue)
			column.pack_start(cell, True)
			column.add_attribute(cell, attr, value)
			#column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			self.treeview.append_column(column)

	def add_package(self, file_list):
		""""""
		id = UploadManager.add_package(self, file_list)
		model = self.treeview.get_model()
		self.treeview.expand_row(model.on_get_path(id), True)

"""(status, name, progress, current_size, total_size, speed, time, info)"""
