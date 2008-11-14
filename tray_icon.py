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

ICON = "media/icon.svg"

class TrayIcon:
    """"""
    def __init__(self):
	""""""
	self.icon = gtk.StatusIcon()
	self.icon.set_tooltip("Tucan!")
	self.icon.set_from_file(ICON)
	self.icon.set_visible(True)
	
	self.menu = gtk.Menu()
	preferences = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
	#preferences.connect('activate', self.preferences_dialog)
	self.menu.append(preferences)
	about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
	#about.connect('activate', self.about_dialog)
	self.menu.append(about)
	separator = gtk.SeparatorMenuItem()
	self.menu.append(separator)
	quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
	quit.connect('activate', self.quit)
	self.menu.append(quit)
	self.menu.show_all()
	
	#self.icon.connect('activate', activate_callback)
	self.icon.connect('popup-menu', self.popup_menu)
	
    def popup_menu(self, statusicon, button, time):
	""""""
	self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.icon)

    def quit(self, dialog=None, response=None):
	""""""
	gtk.main_quit()

if __name__ == "__main__":
    i = TrayIcon()
    gtk.main()