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

import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk

import media
import core.cons as cons

if cons.OS_OSX:
	try:
		from igemacintegration import *
	except Exception:
		pass
	else:
		class OSXDock(MacDock):
			""""""
			def __init__(self, show, quit):
				""""""
				MacDock.__init__(self)
				
				self.show_window = show
				self.window_visible = True
				
				self.connect("quit-activate", quit)
				self.connect("clicked", self.activate)

			def activate(self, statusicon, closed=False):
				""""""
				if self.window_visible:
					if closed:
						self.window_visible = False
				else:
					self.show_window()
					self.window_visible = True

			def close(self):
				""""""
				pass

try:
	import appindicator
except Exception:
	class TrayIcon(gtk.StatusIcon):
		""""""
		def __init__(self, show, hide, menu):
			""""""
			gtk.StatusIcon.__init__(self)
			self.set_tooltip("%s - %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
			self.set_from_file(media.ICON_TUCAN)
			self.set_visible(True)

			self.window_visible = True
			self.show_window = show
			self.hide_window = hide

			self.menu = gtk.Menu()
			for item in menu:
				if item == None:
					tmp = gtk.SeparatorMenuItem()
				else:
					tmp = gtk.ImageMenuItem(item[0])
					tmp.connect('activate', item[1])
				self.menu.append(tmp)
			self.menu.show_all()

			self.connect('activate', self.activate)
			self.connect('popup-menu', self.popup_menu)

		def activate(self, statusicon, event=None):
			""""""
			if self.window_visible:
				self.hide_window()
				self.window_visible = False
			else:
				self.show_window()
				self.window_visible = True

		def popup_menu(self, statusicon, button, time):
			""""""
			self.menu.popup(None, None, None, button, time, self)

		def change_tooltip(self, statusbar, context, text):
			""""""
			#if context == "Downloads":
			tmp = text.split("\t")
			message = "Downloads: " + "".join(tmp[1:]) + "\n" + tmp[0].strip()
			self.set_tooltip(message)

		def close(self):
			""""""
			self.set_visible(False)
else:
	class TrayIcon(appindicator.Indicator):
			""""""
			def __init__(self, show, hide, menu):
				""""""
				appindicator.Indicator.__init__(self,'tucan',media.ICON_TUCAN,appindicator.CATEGORY_APPLICATION_STATUS)
				self.set_status(appindicator.STATUS_ACTIVE)
				icon_theme = gtk.icon_theme_get_default()
				#Try to get the icon from theme
				try:
					pixbuf = icon_theme.load_icon("tucan")
				except:
					pass
				else:
					self.set_icon("tucan")
				self.window_visible = True
				self.show_window = show
				self.hide_window = hide
				
				self.menu = gtk.Menu()
				
				tmp = gtk.MenuItem("Show Tucan")
				tmp.connect('activate',self.show)
				self.menu.append(tmp)
				tmp = gtk.SeparatorMenuItem()
				self.menu.append(tmp)
				
				for item in menu:
					if item == None:
						tmp = gtk.SeparatorMenuItem()
					else:
						tmp = gtk.ImageMenuItem(item[0])
						tmp.connect('activate', item[1])
					self.menu.append(tmp)
				self.menu.show_all()
				self.set_menu(self.menu)
				
			def show(self,arg):
				self.show_window()

			def close(self):
				""""""
				pass
