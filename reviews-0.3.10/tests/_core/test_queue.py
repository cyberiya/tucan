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

from core.queue import Queue

PATH1 = '/home/user/file.part1.rar'
PATH2 = '/home/user/file.part2.rar'
SIZE = 1024
LINK1 = 'megaupload.anonymous_upload'
LINK2 = 'rapidshare.anonymous_upload'

FILE_LIST = [
(PATH1, SIZE, [LINK1, LINK2]), 
(PATH2, SIZE, [LINK1, LINK2])]


class TestQueue(unittest.TestCase):
	""""""
	def setUp(self):
		""""""
		self.queue = Queue()
		self.queue.add_package(FILE_LIST)
			
	def mtest_add_package(self):
		""""""
		#self.queue.add_package()
		for package in self.queue.get_children():
			print package
			for file in self.queue.get_children(package.id):
				print file
				for link in self.queue.get_children(file.id):
					print link

	def test_delete_package(self):
		""""""
		package_id = self.queue.add_package(FILE_LIST)
		packages = self.queue.get_children()
		self.assertEqual(len(packages), 2)
		self.queue.delete(package_id)
		self.assertEqual(len(self.queue.get_children()), 1)
		self.assertEqual(self.queue.get_item(package_id), None)

	def test_delete_file(self):
		""""""
		package_id = self.queue.add_package(FILE_LIST)
		file1, file2 = self.queue.get_children(package_id)
		old_size = self.queue.get_item(package_id).total_size
		self.queue.delete(file1.id)
		size = self.queue.get_item(package_id).total_size
		self.assertEqual(size, old_size-file1.total_size)
		self.assertEqual(len(self.queue.get_children(package_id)), 1)
		self.assertEqual(self.queue.get_item(file1.id), None)
		self.queue.delete(file2.id)
		self.assertEqual(self.queue.get_item(file2.id), None)
		self.assertEqual(self.queue.get_item(package_id), None)

	def test_delete_link(self):
		""""""
		package_id = self.queue.add_package(FILE_LIST)
		file1, file2 = self.queue.get_children(package_id)
		link1, link2 = self.queue.get_children(file1.id)
		p_size = self.queue.get_item(package_id).total_size
		f_size = file1.total_size
		self.queue.delete(link1.id)
		size = self.queue.get_item(file1.id).total_size
		self.assertEqual(size, f_size-link1.total_size)
		size = self.queue.get_item(package_id).total_size
		self.assertEqual(size, p_size-link1.total_size)
		self.assertEqual(len(self.queue.get_children(file1.id)), 1)
		self.assertEqual(self.queue.get_item(link1.id), None)
		self.queue.delete(file2.id)
		self.queue.delete(link2.id)
		self.assertEqual(self.queue.get_item(link2.id), None)
		self.assertEqual(self.queue.get_item(file1.id), None)
		self.assertEqual(self.queue.get_item(package_id), None)

	def test_move_up_package(self):
		""""""
		package_id = self.queue.add_package(FILE_LIST)
		queue = self.queue
		package1, package2 = self.queue.get_children()
		self.queue.move_up(package2)
		self.queue.move_up(package1)
		self.queue.move_up(package1)
		self.assertEqual(self.queue, queue)
		file1, file2 = self.queue.get_children(package1.id)
		self.queue.move_up(file2)
		self.queue.move_up(file1)
		self.queue.move_up(file1)
		self.assertEqual(self.queue, queue)
		link1, link2 = self.queue.get_children(file1.id)
		self.queue.move_up(link2)
		self.queue.move_up(link1)
		self.queue.move_up(link1)
		self.assertEqual(self.queue, queue)
		
	def test_move_down_package(self):
		""""""
		packages = self.queue.get_children()
		files = self.queue.get_children(packages[0].id)
		links = self.queue.get_children(files[1].id)
		self.queue.move_down(packages[0].id)
		

	def tearDown(self):
		""""""
		del self.queue
