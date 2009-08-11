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

import time
import os.path
import xml.etree.ElementTree

import cons

VERSION = "version"
TIMESTAMP = "timestamp"
CLOSED = "closed"

class Session:
	""""""
	def __init__(self):
		""""""
		attrs = {VERSION: cons.TUCAN_VERSION, TIMESTAMP: time.strftime("%Y/%m/%d %H:%M"), CLOSED: "False"}
		self.tree = xml.etree.ElementTree.ElementTree(xml.etree.ElementTree.Element("Session", attrs))

	def load(self):
		""""""
		try:
			self.tree._setroot(self.tree.parse(cons.SESSION_FILE))
		except:
			print "error"
		else:
			print self.tree.getroot()

	def save(self):
		""""""
		self.tree.write(cons.SESSION_FILE)

if __name__ == "__main__":
	s = Session()
	s.save()
	s.load()
