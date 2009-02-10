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

import time

import pygtk
pygtk.require('2.0')
import gtk

from feather_window import FeatherWindow

import cons

class Statusbar(gtk.Statusbar):
	""""""
	def __init__(self, limits):
		""""""
		gtk.Statusbar.__init__(self)
		self.set_has_resize_grip(False)
		
		self.get_limits = limits
		
		self.feather = FeatherWindow()
		
		self.menu = gtk.Menu()
		
		label = gtk.Label("Limits: ")
		self.pack_start(label, False)
		
		button = gtk.Button()
		button.set_image(gtk.Arrow(gtk.ARROW_UP, gtk.SHADOW_NONE))
		self.pack_start(button, False)
				
		button.connect("clicked", self.show_stack)
		self.show_all()
		
	def show_stack(self, widget):
		""""""
		for limit in self.menu:
			self.menu.remove(limit)
		now = time.localtime()
		for plugin, icon_path in self.get_limits():
			limit = gtk.MenuItem()
			if icon_path:
				icon = gtk.image_new_from_file(icon_path)
			else:
				icon = gtk.image_new_from_file(cons.ICON_MISSING)
			limit.add(icon)
			limit.connect("enter-notify-event", self.feather.show_feather, plugin, "[" + str(now[3]) + ":" + str(now[4]) + "]")
			limit.connect("leave-notify-event", self.feather.hide_feather)
			limit.connect("activate", self.feather.hide_feather)
			self.menu.append(limit)
		self.menu.show_all()
		if len(self.menu) > 0:
			self.menu.popup(None, None, self.menu_position, 1, 0, widget.get_allocation())
		
	def menu_position(self, menu, rect):
		""""""
		width, height = menu.size_request()
		window_x, window_y = self.parent.get_parent_window().get_position()
		return rect.x + window_x, rect.y + window_y - height, True

if __name__ == "__main__":
	g = LimitStack()
	gtk.main()