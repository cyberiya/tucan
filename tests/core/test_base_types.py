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

import unittest

NAME = "something"
LINK = "another"
PATH = ""
SIZE = 0

def get_suite():
	suite = []
	suite.append(unittest.TestLoader().loadTestsFromTestCase(TestBase))
	suite.append(unittest.TestLoader().loadTestsFromTestCase(TestContainer))
	suite.append(unittest.TestLoader().loadTestsFromTestCase(TestItem))
	return unittest.TestSuite(suite)

class TestBase(unittest.TestCase):
	def setUp(self):
		from core.base_types import Base
		self.base = Base(NAME)
		
	def test_id(self):
		self.assertEqual(len(self.base.get_id()), 36, "id should have 36 characters")
	
	def test_name(self):
		self.assertTrue(self.base.get_name(), "name should not be empty")
				
	def tearDown(self):
		del self.base

class TestContainer(unittest.TestCase):
	def setUp(self):
		from core.base_types import Container
		self.container = Container()
		
	def test_(self):
		pass
					
	def tearDown(self):
		del self.container

class TestItem(unittest.TestCase):
	def setUp(self):
		from core.base_types import Item
		self.item = Item(NAME, PATH, SIZE)
				
	def test_set_name(self):
		self.item.set_name(LINK)
		self.assertNotEqual(self.item.get_name(), NAME, "name should be updated")	
		self.assertEqual(self.item.get_name(), LINK, "name should be updated")	
		
	def tearDown(self):
		del self.item
