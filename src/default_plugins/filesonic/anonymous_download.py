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
import cookielib

import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen

BASE_URL = "http://filesonic.com/file"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			file_id = url.split("/")[-2]
			form_action = "%s/%s/%s?start=1" % (BASE_URL,file_id,file_id)
			
			if not wait_func():
				return
			
			it = opener.open(form_action)
			it_tmp = None
			for line in it:
				#First wait
				if "name='tm'" in line:
					tm = line.split("value='")[1].split("'")[0];
					tm_hash = it.next().split("value='")[1].split("'")[0];
					form = urllib.urlencode([("tm", tm), ("tm_hash", tm_hash)])
					it_tmp = opener.open(form_action, form)
					break
			
			#Loop until we get the captcha
			for loop in range(3):
				if not wait_func():
					return
				if it_tmp:
					it = it_tmp
				else:
					it = opener.open(form_action)
				for line in it:
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
								it = opener.open(form_action, form, content_range)
								#Get the link
								for line in it:
									if 'downloadLink' in line:
										it.next()
										return opener.open(it.next().split('href="')[1].split('"')[0])
				
					#Link already there
					elif 'downloadLink' in line:
						it.next()
						return opener.open(it.next().split('href="')[1].split('"')[0])
					
					if "name='tm'" in line:
						tm = line.split("value='")[1].split("'")[0];
						tm_hash = it.next().split("value='")[1].split("'")[0];
						form = urllib.urlencode([("tm", tm), ("tm_hash", tm_hash)])
						it_tmp = opener.open(form_action, form)
				
					#Need to wait
					elif 'countDownDelay =' in line:
						wait = int(line.split("= ")[1].split(";")[0])
						if wait < 60:
							if not wait_func(wait):
								return
							#Next loop, reload the page
							break
						else:
							return self.set_limit_exceeded(wait)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = URLOpen().open(url)
			for line in it:
				if 'fileInfo filename' in line:
					name = line.split('<strong>')[1].split('</strong>')[0]
				elif 'fileInfo filesize' in line:
					it.next()
					it.next()
					tmp = it.next().split('class="size">')[1].split("<")[0]
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
