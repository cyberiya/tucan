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

import time
import os.path
import unittest
import ConfigParser

import __builtin__
from core.events import Events
__builtin__.events = Events()

import core.cons as cons

ACCOUNTS_FILE = "test.accounts"

OPTION_NAME = "name"
OPTION_PASSWORD = "password"

TEST_DIR = "/tmp/"
TEST_NAME = "prueba.bin"

class TestBaseDownload(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.plugin = None
		self.invalid_link = None
		self.link = None
		self.size = None
		self.unit = None

	def check_link(self, link, name, size, unit):
		""""""
		n, s, u = self.plugin.check_links(link)
		self.assertEqual(n, name, "%s != %s" % (n, name))
		self.assertEqual(s, size, "%s != %i" % (s, size))
		self.assertEqual(u, unit, "%s != %s" % (u, unit))
		
	def test_check_invalid_link(self):
		""""""
		self.check_link(self.invalid_link, None, -1, None)

	def test_check_valid_link(self):
		""""""
		self.check_link(self.link, TEST_NAME, self.size, self.unit)

	def test_download(self):
		""""""
		self.check_link(self.link, TEST_NAME, self.size, self.unit)
		self.assertTrue(self.plugin.add(TEST_DIR, self.link, TEST_NAME), "check slots or limits")
		status = cons.STATUS_WAIT
		while ((status != cons.STATUS_ERROR) and (status != cons.STATUS_CORRECT)):
			status, progress, actual_size, unit, speed, time_ = self.plugin.get_status(TEST_NAME)
			time.sleep(1)
		self.assertEqual(status, cons.STATUS_CORRECT, "s%: Error downloading")
		name = "%s%s" % (TEST_DIR, TEST_NAME)
		self.assertTrue(os.path.exists(name), "Not Found: %s" % name)
		f1 = file(os.path.join("_default_plugins", TEST_NAME), "r")
		f2 = file(name, "r")
		local = f1.read()
		remote = f2.read()
		f1.close()
		f2.close()
		os.remove(name)
		self.assertEqual(local, remote, "%i != %i" % (len(local), len(remote)))

class TestBaseCookie(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.cookie = None
		self.service_name = ""

	def get_mocked_config(self, config):
		""""""
		account_name, account_password = self.get_account_data()
		if account_name and account_password:
			config.get_accounts = lambda x: {account_name: (account_password, True, True)}
		return config
	
	def get_account_data(self):
		"""
		ACCOUNTS_FILE should be populated like this:
		
		[service_name]
		name = something
		password = something_else
		
		"""
		account_name = ""
		account_password = ""
		
		name = os.path.join("_default_plugins", ACCOUNTS_FILE)
		self.assertTrue(os.path.exists(name), "Not Found: %s" % name)
		
		config = ConfigParser.SafeConfigParser()
		
		try:
			config.read(name)
			account_name = config.get(self.service_name, OPTION_NAME)
			account_password = config.get(self.service_name, OPTION_PASSWORD)
		except Exception, e:
			self.fail(e)
		else:
			self.assertTrue(account_name, "Name shouldn't be empty")
			self.assertTrue(account_password, "Password shouldn't be empty")
		return account_name, account_password

	def test_invalid_cookie(self):
		""""""
		self.assertFalse(self.cookie.get_cookie("", ""), "Cookie should be None")

	def test_valid_cookie(self):
		""""""
		account_name, account_password = self.get_account_data()
		self.assertTrue(self.cookie.get_cookie(account_name, account_password), "Cookie shouldn't be None")
