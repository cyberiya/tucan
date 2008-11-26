 # -*- coding: iso-8859-15 -*-
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

import cons

NAME = "Tucan"
COPYRIGHT = u"© 2008 The Tucan Project"
WEBPAGE = "http://cusl3-tucan.forja.rediris.es/"
AUTHORS = ["Fran Lupion Crakotak@yahoo.es", "Paco Salido beakman@riseup.net", "JM Cordero betic0@gmail.com"]
LICENSE = """	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	"""

class About(gtk.AboutDialog):
	""""""
	def __init__(self, widget=None):
		""""""
		gtk.AboutDialog.__init__(self)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_icon_from_file(cons.ICON_TUCAN)
		self.set_logo(gtk.gdk.pixbuf_new_from_file(cons.ICON_TUCAN))
		self.set_name(NAME)
		self.set_version(cons.TUCAN_VERSION)
		self.set_copyright(COPYRIGHT)
		self.set_license(LICENSE)
		self.set_website(WEBPAGE)
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()

if __name__ == "__main__":
	g = About()
	gtk.main()