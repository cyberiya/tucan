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

import sys
sys.path.append("/home/crak/tucan/trunk")
import __builtin__
__builtin__.PROXY = None

from core.url_open import URLOpen

import core.cons as cons

API_URL = "http://api.rapidshare.com/cgi-bin/rsapi.cgi"

class CheckLinks:
	""""""
	def check(self, url, max_size=None):
		""""""
		name = None
		size = -1
		unit = None
		try:
			tmp = URLOpen().open(API_URL, self.prepare_data([url])).readlines()
			link_list = self.extract_link_info(tmp, max_size)
			if link_list:
				name = link_list[0][0]
				size = link_list[0][1]
				unit = link_list[0][2]
		except Exception, e:
			logger.exception(e)
		return name, size, unit

	def prepare_data(self, urls):
		""""""
		files = []
		filenames = []
		for url in urls:
			tmp_url = url.split("/")
			filenames.append(tmp_url.pop())
			files.append(tmp_url.pop())
		data = urllib.urlencode([("sub", "checkfiles_v1"), ("files", ",".join(files)), ("filenames", ",".join(filenames))])
		return data
		
	def extract_link_info(self, lines, max_size):
		""""""
		result = []
		for line in lines:
			name = None
			size = -1
			unit = None
			if "ERROR" not in line:
				info = line.split(",")
				status = int(info[4])
				if status == 1 or status == 2 or status == 6:
					name = info[1]
					if max_size:
						if int(info[2]) <= max_size:
							size, unit = self.get_size(int(info[2]))
					else:
							size, unit = self.get_size(int(info[2]))
						
				result.append((name, size, unit))
		return result
		
	def get_size(self, num):
		"""on 0.3.10 will be part of misc.py"""
		result = 0, cons.UNIT_KB
		if num:
			result = 1, cons.UNIT_KB
			tmp = int(num/1024)
			if  tmp > 0:
				result = tmp, cons.UNIT_KB
				tmp = int(tmp/1024)
				if tmp > 0:
					result = tmp, cons.UNIT_MB
		return result

if __name__ == "__main__":
	urls = ["http://rapidshare.com/files/28369474/30_-_Buscate_la_Vida_-_Novia_2000_by_shagazz.part1.exe",
		"http://rapidshare.com/files/279692839/The.Shield.S04E04.WS.DVDRip.XviD-SAiNTS.avi",
		"http://rapidshare.com/files/389459308/The.Losers.DvdScr.2010.by.abel_21.part09.rar.html"]
	for url in urls:
		#print CheckLinks().check(url)
		print CheckLinks().check(url, 209796096)
