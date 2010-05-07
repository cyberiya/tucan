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

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "../")))

TEST_PREFIX = "test_"
TEST_SUFIX = ".py"
PATH_SEPARATOR = "/"

def get_suite():
	suite = []
	suite.append(unittest.TestLoader().loadTestsFromTestCase(TestBase))
	suite.append(unittest.TestLoader().loadTestsFromTestCase(TestContainer))
	suite.append(unittest.TestLoader().loadTestsFromTestCase(TestItem))
	return unittest.TestSuite(suite)

class Suite:
	""""""
	def __init__(self):
		""""""
		self.loader = unittest.TestLoader()
		self.tmp_suite = []
		
	def get_suite(self, path):
		""""""
		if len(path) == 0:
			path = os.listdir(".")
		self.recursive_walk_suites(path)
		return unittest.TestSuite(self.tmp_suite)

	def add_tests(self, name):
		""""""
		module_name = ".".join(name.split(TEST_SUFIX)[0].split(PATH_SEPARATOR))
		print module_name
		self.tmp_suite.append(self.loader.loadTestsFromName(module_name))

	def recursive_walk_suites(self, names, parent=""):
		""""""
		if not isinstance(names, list):
			if os.path.basename(names).startswith(TEST_PREFIX) and names.endswith(TEST_SUFIX):
				self.add_tests(names)
		elif len(names) > 0:
			for path in names:
				path = os.path.join(parent, path)
				if os.path.isdir(path) and not os.path.basename(path).startswith("."):
					self.recursive_walk_suites(os.listdir(path), path)
				else:
					self.recursive_walk_suites(path)

if __name__ == '__main__':	
	import optparse
	parser = optparse.OptionParser()
	parser.add_option("-l", "--logging", dest="level", help="set logger LEVEL (default=ERROR)", metavar="LEVEL")
	parser.add_option("-v", "--verbosity", dest="verbosity", help="set verbosity LEVEL (default=1)", metavar="LEVEL")
	options, args = parser.parse_args()

	import logging
	logging.basicConfig(level=logging.ERROR)
	
	s = Suite()
	print s.get_suite(args)
		
	#unittest.TextTestRunner(verbosity=2).run(get_all())
	#unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestEvents))
