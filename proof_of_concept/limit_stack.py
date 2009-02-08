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

import pygtk
pygtk.require('2.0')
import gtk

from custom_window import FeatherWindow

class LimitStack(gtk.Window):
	""""""
	def __init__(self, widget=None):
		""""""
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(300, -1)
		self.set_decorated(False)
		statusbar = gtk.Statusbar()
		statusbar.set_has_resize_grip(False)
		self.add(statusbar)
		button = gtk.Button()
		button.set_image(gtk.Arrow(gtk.ARROW_UP, gtk.SHADOW_NONE))
		statusbar.pack_start(button, False)
		
		feather = FeatherWindow(self)
		
		self.menu = gtk.Menu()
		for item in [1,2]:
			tmp = gtk.MenuItem(" - ")
			tmp.connect("enter-notify-event", feather.show_feather)
			tmp.connect("leave-notify-event", feather.hide_feather)
			self.menu.append(tmp)
		self.menu.show_all()
		button.connect("clicked", self.show_stack)
		self.show_all()
				
	def show_stack(self, widget):
		""""""
		self.menu.popup(None, None, self.menu_position, 1, 0, widget.get_allocation())
		
	def menu_position(self, menu, rect):
		""""""
		width, height = menu.size_request()
		window_x, window_y = self.get_position()
		return rect.x + window_x, rect.y + window_y - height, True

if __name__ == "__main__":
	g = LimitStack()
	gtk.main()