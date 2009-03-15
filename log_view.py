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
import gobject

import cons

SEVERITY = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class LogView(gtk.Dialog):
	""""""
	def __init__(self, widget=None):
		""""""
		gtk.Dialog.__init__(self)
		self.set_title("Log View")
		self.set_size_request(700,500)
		self.set_icon(self.render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU))

		self.file = open(cons.LOG_FILE, "r")
		self.back_buffer = gtk.TextBuffer()
		self.back_buffer.set_text(self.file.read())

		#textview
		frame = gtk.Frame()
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		hbox = gtk.HBox()
		frame.add(hbox)
		
		#auto scroll 
		scroll = gtk.ScrolledWindow()
		hbox.pack_start(scroll)
		scroll.get_vadjustment().connect("changed", self.changed)
		scroll.get_vadjustment().connect("value-changed", self.value_changed)		
		
		scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.textview = gtk.TextView(gtk.TextBuffer())
		scroll.add(self.textview)
		self.textview.set_wrap_mode(gtk.WRAP_CHAR)
		self.textview.set_editable(False)
		
		#combo
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 10)
		buttonbox = gtk.HButtonBox()
		hbox.pack_start(buttonbox, False, False, 10)
		label = gtk.Label("Minimum severity shown.")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		
		self.combo = gtk.combo_box_new_text()
		buttonbox.pack_start(self.combo)
		self.combo.connect("changed", self.reload)
		
		for s in SEVERITY:
			self.combo.append_text(s)
		self.combo.set_active(2)
		
		#action area
		button = gtk.Button(None, gtk.STOCK_CLOSE)
		self.action_area.pack_start(button)
		button.connect("clicked", self.close)

		self.connect("response", self.close)
		self.show_all()
		
		gobject.timeout_add(1000, self.update)
		self.run()
	
	def reload(self, textview):
		""""""
		buffer = self.textview.get_buffer()
		buffer.set_text("")
		ini, fin = self.back_buffer.get_bounds()
		for line in self.back_buffer.get_text(ini, fin).split("\n"):
			for s in SEVERITY[self.combo.get_active():]:
				if s in line:
					buffer.insert(buffer.get_end_iter(), line + "\n")
					break
	
	def update(self):
		""""""
		try:
			line = self.file.readline()
			self.back_buffer.insert(self.back_buffer.get_end_iter(), line)
			buffer = self.textview.get_buffer()
			for s in SEVERITY[self.combo.get_active():]:
				if s in line:
					buffer.insert(buffer.get_end_iter(), line)
					break
		except:
			pass
		else:
			return True
		
	def changed(self, vadjust):
		""""""
		if not hasattr(vadjust, "need_scroll") or vadjust.need_scroll:
			vadjust.set_value(vadjust.upper-vadjust.page_size)
			vadjust.need_scroll = True

	def value_changed (self, vadjust):
		""""""
		vadjust.need_scroll = abs(vadjust.value + vadjust.page_size - vadjust.upper) < vadjust.step_increment
		
	def close(self, widget=None, other=None):
		""""""
		self.file.close()
		self.destroy()

if __name__ == "__main__":
	c = LogView()
