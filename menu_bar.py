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

class MenuBar(gtk.MenuBar):
	""""""
	def __init__(self, list):
		"""list = [(menu_name=str, [(item_image=stock_item, callback), None=separator])]"""
		gtk.MenuBar.__init__(self)
		for menu in list:
			item = gtk.MenuItem(menu[0])
			self.append(item)
			submenu = gtk.Menu()
			for sub in menu[1]:
				if sub == None:
					subitem = gtk.SeparatorMenuItem()
				else:
					subitem = gtk.ImageMenuItem(sub[0])
					subitem.connect("activate", sub[1])
				submenu.append(subitem)
			item.set_submenu(submenu)