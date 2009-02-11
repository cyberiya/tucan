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

import urllib
import urllib2

from HTMLParser import HTMLParser

HEADER = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4"}
BUFFER_SIZE = 4096

class UploadParser(HTMLParser):
	""""""
	def __init__(self, file_name, description):
		""""""
		HTMLParser.__init__(self)
		self.action = None
		self.id = None
		self.feed(urllib2.urlopen(urllib2.Request("http://www.megaupload.com/")).read())
		self.close()
		if self.action:
			form = {"UPLOAD_IDENTIFIER": self.id, "sessionid": self.id , "file": file(file_name, "rb"), "message": description, "accept": 1}
			handle = urllib2.urlopen(urllib2.Request("http://www.megaupload.com/", None, HEADER), urllib.urlencode(form))
			print handle.info()
			for line in handle.readlines():
				if "downloadurl" in line:
					print line

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if attrs[1][1] == "uploadprogress":
				self.action = attrs[3][1]
		elif tag == "input":
			if attrs[1][1] == "UPLOAD_IDENTIFIER":
				self.id = attrs[2][1]

if __name__ == "__main__":
	c = UploadParser("/home/crak/2009-02-10-231803_1024x600_scrot.png", "mierda")