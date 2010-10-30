###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen

BASE_URL = "http://easy-share.com"

class AnonymousDownload(DownloadPlugin):
	""""""
	#FIXME : change range which is a keyword
	def link_parser(self, url, wait_func, xrange=None):
		""""""
		try:
			data = urllib.urlencode([("free", "Regular Download")])
			url = "%sbilling?%s" % (url,data)
			opener = URLOpen()
			it = iter(opener.open(url,data).readlines())
			for line in it:
				if 'name="id"' in line:
					file_id = line.split('value="')[1].split('"')[0]
				if 'id="dwait"' in line:
					tmp = it.next()
					#The download is possible
					if "form" in tmp:
						form_action = tmp.split('action="')[1].split('"')[0]
					#Necessary to wait
					else:
						it.next()
						it.next()
						wait = it.next().split("'")[1].split("'")[0]
						self.set_limit_exceeded(int(wait))
						return
				if 'Recaptcha.create("' in line:
					tmp = line.split('"')[1].split('"')[0]
					recaptcha_link = "http://www.google.com/recaptcha/api/challenge?k=%s" % tmp
					if not wait_func():
						return
					c = Recaptcha(BASE_URL, recaptcha_link)
					for retry in range(3):
						challenge, response = c.solve_captcha()
						if response:
							if not wait_func():
								return
							
							#Submit the input to the recaptcha system
							form = urllib.urlencode([("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response), ("recaptcha_shortencode_field", "undefined")])
							handle = opener.open(form_action, form)
							if not handle.info().getheader("Content-Type") == "text/html":
								#Captcha is good
								return handle
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = iter(URLOpen().open(url).readlines())
			for line in it:
				if '<span class="txtorange">' in line:
					tmp = it.next()
					name = tmp.split("<")[0].strip()
					tmp = tmp.split(">(")[1].split(")")[0]
					if "KB" in tmp:
						size = int(round(float(tmp.split("KB")[0])))
						unit = "KB"
					elif "MB" in tmp:
						size = float(tmp.split("MB")[0])
						if int(round(size)) > 0:
							size = int(round(size))
							unit = "MB"
						else:
							size = int(round(1024 * size))
							unit = "KB"
					elif "GB" in tmp:
						size = int(round(float(tmp.split("GB")[0])))
						unit = "GB"
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
