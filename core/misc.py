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

import re
import sys
import urllib
import logging
logger = logging.getLogger(__name__)

from htmlentitydefs import name2codepoint

import url_open
import cons

REPORT_URL = "http://crak.appspot.com/add"

def main_info(log=logger):
	""""""
	log.info("%s %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
	log.debug("OS: %s" %  cons.OS_VERSION)
	log.debug("PYTHON: %s" % cons.OS_PYTHON)
	log.debug("Main path: %s" % cons.PATH)
	log.debug("Configuration path: %s" % cons.CONFIG_PATH)

def report_log(email="", comment=""):
	""""""
	try:
		f = open(cons.LOG_FILE, "r")
		log = f.read()
		f.close()
	except Exception, e:
		logger.exception("%s" % e)
	else:
		form = urllib.urlencode([("uuid", configuration.get_uuid()), ("email", email), ("comment", urllib.quote(comment)), ("log", urllib.quote(log))])
		try:
			id = url_open.URLOpen().open(REPORT_URL, form).read().strip()
			logger.info("REPORT ID: %s" % id)
		except Exception, e:
			logger.exception("Could not report: %s" % e)
		else:
			return id

def get_exception_info(type, value, trace):
	""""""
	try:
		file_name = trace.tb_frame.f_code.co_filename
		line_no = trace.tb_lineno
		exception = type.__name__
	except:
		return "Unhandled Error! No info available"
	else:
		return "File %s line %i - %s: %s" % (file_name, line_no, exception, value)

def url_quote(url):
	"""Replace special characters in string using the %xx escape. """
	return urllib.quote(url, "/:=?")
	
def url_unquote(url):
	"""Replace %xx escapes by their single-character equivalent."""
	return urllib.unquote(urllib.unquote(url))

def substitute_entity(match):
	""""""
	ent = match.group(2)
	if match.group(1) == "#":
		return unichr(int(ent))
	else:
		cp = name2codepoint.get(ent)
	if cp:
		return unichr(cp)
	else:
		return match.group()

def decode_htmlentities(string):
	""""""
	#entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
	#return entity_re.subn(substitute_entity, string)[0]
	return string