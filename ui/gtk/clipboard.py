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

import HTMLParser
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import sys
sys.path.append("/home/crak/tucan/trunk/")

import core.cons as cons

def check_contents(clipboard, selection_data):
	""""""
	urls = []
	if cons.OS_OSX:
		target_html = "public.rtf"
		if target_html  in list(selection_data):
			selection = clipboard.wait_for_contents(target_html)
			if selection:
				for line in str(selection.data.decode("utf8", "ignore")).split("\n"):
					if '{HYPERLINK "' in line:
						urls.append(line.split('{HYPERLINK "')[1].split('"}')[0])
	elif cons.OS_WINDOWS:
		target_html = "HTML Format"
		if target_html in list(selection_data):
			try:
				parser = ClipParser()
				parser.feed(clipboard.wait_for_contents(target_html).data.decode("utf8", "ignore"))
				parser.close()
				if len(parser.url) > 0:
					urls += parser.url
			except HTMLParser.HTMLParseError:
				pass
	else:
		target_html = "text/html"
		if target_html  in list(selection_data):
			for line in str(clipboard.wait_for_contents(target_html).data.decode("utf16", "ignore")).split("\n"):
				try:
					parser = ClipParser()
					parser.feed(line)
					parser.close()
					if len(parser.url) > 0:
						urls += parser.url
				except HTMLParser.HTMLParseError:
					pass
	return urls

class ClipParser(HTMLParser.HTMLParser):
	""""""
	def __init__(self):
		""""""
		HTMLParser.HTMLParser.__init__(self)
		self.url = []

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			for ref, link in attrs:
				if ref == "href":
					self.url.append(link)
					
class Clipboard:
	""""""
	def __init__(self, parent, callback, services):
		""""""
		self.monitor_active = False
		self.monitor = ClipboardMonitor(parent)
		self.content_callback = callback
		self.services = services
		gobject.timeout_add(1000, self.poll_clipboard)
		
	def show_monitor(self, clipboard, selection_data, data):
		""""""
		urls = check_contents(clipboard, selection_data)
		if len(urls) > 0:
			links = []
			for url in urls:
				for name in self.services:
					if url.find(name) > 0:
						links.append(url)
						break
			if len(links) > 0:
				clipboard.set_text("", 0)
				self.monitor.open(links)
				content = self.monitor.get_content()
				if content:
					self.content_callback(None, content)
		self.monitor_active = False

	def poll_clipboard(self):
		""""""
		if not self.monitor_active:
			self.monitor_active = True
			clipboard = gtk.clipboard_get()
			clipboard.request_targets(self.show_monitor)
		return True


class ClipboardMonitor(gtk.Dialog):
	""""""
	def __init__(self, parent):
		""""""
		gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.set_icon(self.render_icon(gtk.STOCK_PASTE, gtk.ICON_SIZE_MENU))
		self.set_title("%s - %s" % (cons.TUCAN_NAME, ("Clipboard Monitor")))
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(400,200)

		#textview
		frame = gtk.Frame(("Supported links:"))
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		hbox = gtk.HBox()
		frame.add(hbox)
		scroll = gtk.ScrolledWindow()
		hbox.pack_start(scroll, True, True)
		scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		buffer = gtk.TextBuffer()
		self.textview = gtk.TextView(buffer)
		scroll.add(self.textview)
		self.textview.set_wrap_mode(gtk.WRAP_CHAR)
		
		self.content = None
		
		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		add_button = gtk.Button(None, gtk.STOCK_ADD)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(add_button)
		cancel_button.connect("clicked", self.close)
		add_button.connect("clicked", self.set_content)

		self.connect("response", self.close)
		
	def set_content(self, button=None):
		""""""
		buffer = self.textview.get_buffer()
		start, end = buffer.get_bounds()
		self.content = buffer.get_text(start, end)
		self.close()
		
	def get_content(self):
		""""""
		result = self.content
		self.content = None
		return result
		
	def open(self, links):
		""""""
		self.textview.get_buffer().insert_at_cursor("\n".join(links) + "\n")
		self.show_all()
		self.run()
		
	def close(self, widget=None, other=None):
		""""""
		self.hide()
		self.textview.get_buffer().set_text("")
