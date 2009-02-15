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

import HTMLParser
import threading

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import cons

class InputLinks(gtk.Dialog):
	""""""
	def __init__(self, path, sort, check, create, manage, show_advanced_packages):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_DOWNLOAD)
		self.set_title(_("Input Links"))
		self.set_size_request(600,500)
		

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = InputFiles()
	gtk.main()