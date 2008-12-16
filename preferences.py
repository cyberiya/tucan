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

class Preferences(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon(self.render_icon(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU))
		self.set_title("Preferences")
		self.set_size_request(500,500)
		
		self.notebook = gtk.Notebook()
		self.notebook.set_property("homogeneous", True)
		self.vbox.pack_start(self.notebook)
		self.new_page("General Configuration", cons.ICON_PREFERENCES_MAIN, self.init_main())
		self.new_page("Service Configuration", cons.ICON_PREFERENCES_SERVICES, self.init_services())
		self.new_page("Advanced Configuration", cons.ICON_PREFERENCES_ADVANCED, self.init_advanced())

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		save_button = gtk.Button(None, gtk.STOCK_SAVE)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(save_button)
		cancel_button.connect("clicked", self.close)
		save_button.connect("clicked", self.close)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def new_page(self, tab_name, tab_image, page):
		""""""
		vbox = gtk.VBox()
		vbox.pack_start(gtk.image_new_from_file(tab_image))
		vbox.pack_start(gtk.Label(tab_name))
		vbox.show_all()
		self.notebook.append_page(page, vbox)
		self.notebook.set_tab_label_packing(page, True, True, gtk.PACK_START)
		
	def init_main(self):
		""""""
		vbox = gtk.VBox()
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_NETWORK))
		vbox.pack_start(frame, False, False)
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		
		hbox = gtk.HBox()
		label = gtk.Label("Max simultaneous downloads: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		spinbutton = gtk.SpinButton()
		spinbutton.set_range(1,10)
		spinbutton.set_increments(1,0)
		spinbutton.set_numeric(True)
		hbox.pack_start(spinbutton, False, False, 10)
		vbox1.pack_start(hbox, False, False, 5)
		
		hbox = gtk.HBox()
		label = gtk.Label("Max simultaneous uploads: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		spinbutton = gtk.SpinButton()
		spinbutton.set_range(1,10)
		spinbutton.set_increments(1,0)
		spinbutton.set_numeric(True)
		hbox.pack_start(spinbutton, False, False, 10)
		vbox1.pack_start(hbox, False, False, 5)
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_FOLDER))
		vbox.pack_start(frame, False, False)
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_LANGUAGE))
		vbox.pack_start(frame, False, False)
		vbox.show_all()
		return vbox

	def init_services(self):
		""""""
		return gtk.VBox()
		
	def init_advanced(self):
		""""""
		return gtk.VBox()
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = Preferences()