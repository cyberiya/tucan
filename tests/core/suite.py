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

import unittest

import sys
#sys.path.append("/Users/Crak/Desktop/tucan/trunk")
sys.path.append("/home/crak/tucan/trunk")

import test_base_types
import test_download_types

def get_all():
	suite = []
	suite.append(get_types())
	return unittest.TestSuite(suite)

def get_types():
	suite = []
	suite.append(test_base_types.get_suite())
	suite.append(test_download_types.get_suite())
	return unittest.TestSuite(suite)

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.CRITICAL)
	unittest.TextTestRunner(verbosity=2).run(get_all())
