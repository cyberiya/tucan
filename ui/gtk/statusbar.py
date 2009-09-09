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

import __builtin__
import gettext

import time
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import cons
import media

class Statusbar(gtk.Statusbar):
	""""""
	def __init__(self, limits):
		""""""
		gtk.Statusbar.__init__(self)
		self.set_has_resize_grip(False)

		#download speed limit
		frame = gtk.Frame()
		self.pack_start(frame, False, False)
		hbox = gtk.HBox()
		frame.add(hbox)
		label = gtk.Label(_("Max speed: "))
		hbox.pack_start(label)
		self.max_speed = gtk.SpinButton(None, 4, 0)
		self.max_speed.set_property("shadow-type", gtk.SHADOW_NONE)
		self.max_speed.set_range(0,5000)
		self.max_speed.set_increments(4,0)
		self.max_speed.set_numeric(True)
		self.max_speed.set_value(__builtin__.max_download_speed)
		hbox.pack_start(self.max_speed, False, False, 5)

		self.max_speed.connect("value-changed", self.change_speed)

		#show limits
		self.get_limits = limits

		self.menu = gtk.Menu()

		label = gtk.Label("Limits: ")
		self.pack_start(label, False)

		self.button = gtk.Button()
		self.button.set_image(gtk.Arrow(gtk.ARROW_UP, gtk.SHADOW_NONE))
		self.pack_start(self.button, False)

		self.limits = []
		self.max_limits = 0

		self.blinking = False
		self.white = True
		self.button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#fff"))

		self.button.connect("clicked", self.show_stack)
		self.show_all()

		gobject.timeout_add(60000, self.update_limits)

	def synchronize(self):
		""""""
		self.max_speed.set_value(__builtin__.max_download_speed)

	def change_speed(self, spinbutton):
		""""""
		__builtin__.max_download_speed = spinbutton.get_value_as_int()

	def update_limits(self):
		""""""
		self.limits = self.get_limits()
		if len(self.limits) > self.max_limits:
			if not self.blinking:
				gobject.timeout_add(800, self.blink)
				self.blinking = True
			logger.debug("Limits: %s" % self.limits)
		self.max_limits = len(self.limits)
		return True

	def blink(self):
		""""""
		if self.white:
			if self.blinking:
				self.button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#f99"))
				self.white = False
				return True
			else:
				return False
		else:
			self.button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#fff"))
			self.white = True
			if self.blinking:
				return True
			else:
				return False

	def show_stack(self, widget):
		""""""
		self.blinking = False
		for limit in self.menu:
			self.menu.remove(limit)
		self.limits = self.get_limits()
		if len(self.limits) == 0:
			self.limits = [("None", "", "", None)]
		for service, type, hour, icon_path in self.limits:
			limit = gtk.MenuItem()
			vbox = gtk.VBox()
			hbox = gtk.HBox()
			if icon_path:
				icon = gtk.gdk.pixbuf_new_from_file(icon_path)
			else:
				icon = gtk.gdk.pixbuf_new_from_file(media.ICON_MISSING)
			hbox.pack_start(gtk.image_new_from_pixbuf(icon.scale_simple(24, 24, gtk.gdk.INTERP_BILINEAR)))
			hbox.pack_start(gtk.Label(service), True, True, 5)
			vbox.pack_start(hbox, True, False, 1)
			hbox = gtk.HBox()
			hbox.pack_start(gtk.Label(hour), True, True)
			hbox.pack_start(gtk.Label(type), True, True, 5)
			vbox.pack_start(hbox)
			limit.add(vbox)
			self.menu.append(limit)
			self.menu.append(gtk.SeparatorMenuItem())
		self.menu.show_all()
		self.menu.popup(None, None, self.menu_position, 1, 0, widget.get_allocation())

	def menu_position(self, menu, rect):
		""""""
		width, height = menu.size_request()
		window_x, window_y = self.parent.get_parent_window().get_position()
		return rect.x + window_x - (width - rect.width), rect.y + window_y - height, True

if __name__ == "__main__":
	g = LimitStack()
	gtk.main()
