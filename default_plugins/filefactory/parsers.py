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

import urllib
import logging
logger = logging.getLogger(__name__)

from core.url_open import URLOpen

BASE_URL = "http://www.filefactory.com"

class Parser:
	def __init__(self, url):
		""""""
		self.link = None
		self.wait = None
		try:
			button_action = self.get_link(url)
			if button_action:
				link = self.solve_javascript(button_action)
				tmp_link = self.get_link(link)
				self.link = self.solve_javascript(tmp_link)
		except Exception, e:
			logger.exception("%s :%s" % (url, e))

	def get_link(self, url):
		""""""
		result = None
		for line in URLOpen().open(url).readlines():
			if '/file/getLink.js' in line:
				result = "%s/file/getLink.js%s" % (BASE_URL, line.split(",")[1].split('"')[1])
			elif "startWait" in line:
				self.wait = int(line.split('value="')[1].split('"')[0])
		return result

	def solve_javascript(self, url):
		""""""
		tmp = URLOpen().open(url).readlines()[1].split("{")
		vars = {}
		for var in tmp[1].split(";"):
			if not "function()" in var:
				var = var.split("=")
				vars[var[0].split("var")[1].strip()] = var[1].split("'")[1].strip()
		tmp = tmp[2].split(";")[0].split("'")
		tmp_link = ""
		if tmp[1]:
			base = tmp[1]
		else:
			base = BASE_URL
		for var in tmp[2].split("+"):
			if var in vars:
				tmp_link += vars[var]
		return "%s%s%s" % (base, tmp_link, tmp[3])

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in URLOpen().open(url).readlines():
				if '<span class="last">' in line:
					name = line.split('<span class="last">')[1].split('</span>')[0]
					if ".." in name:
						tmp = url.split("/").pop().split("_")
						name = ".".join(tmp)
				elif "file uploaded" in line:
					tmp = line.split("file uploaded")[0].split("<span>")[1].split(" ")
					size = int(float(tmp[0]))
					if size == 0:
						size = 1
					unit = tmp[1]
			if not name:
				name = url
				size = -1
		except Exception, e:
			name = url
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	c = Parser("http://www.filefactory.com/file/ah324b7/n/06_Massive_Attack_amp_Portishead_-_Improvisation_amp_Glory_Box.mp3")
	#c = Parser("http://www.filefactory.com/file/a0h9c7a/n/Just_M_-_Njene_sanje_Hocem_sosedo_-_karaoke.mp3")
	print c.link, c.wait
	#print CheckLinks().check("http://www.filefactory.com/file/cc646e/n/Music_Within_2007_Sample_avi")
	#print CheckLinks().check("http://www.filefactory.com/file/4460d3/n/Intelligent_Sounds_Music_BazzISM_VSTi_v2_0d_MAC_OSX_UB_Incl_Keygen-ArCADE_rar")
