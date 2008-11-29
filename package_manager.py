###############################################################################
##	Tucan Project

##	Copyright (C) 2008 Fran Lupion Crakotak(at)yahoo.es
##	Copyright (C) 2008 Paco Salido beakman(at)riseup.net
##	Copyright (C) 2008 JM Cordero betic0(at)gmail.com

##	This program is free software; you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation; either version 2 of the License, or
##	(at your option) any later version.

##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.

##	You should have received a copy of the GNU General Public License
##	along with this program; if not, write to the Free Software
##	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import re

import cons

LINKS = {'megaupload.com': [('http://www.megaupload.com/?d=N06UYST6', 'D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=HE4TMQPQ', 'D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=3TSDC4J3', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=BP5RK0TM', 'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=2XF7ELQ9', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=15YBBMCG', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 68, 'MB', 'AnonymousMegaupload')], 'rapidshare.com': [('http://rapidshare.com/files/151319465/D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319467/D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319554/D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319448/D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319452/D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319357/D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 69, 'MB', 'PremiumRapidshare')]}

class PackageManager:
	""""""
	def __init__(self):
		""""""
		pass
	
	def create_packages(self, dict):
		"""packages [(name, links)]"""
		packages = []
		files = []
		for service, links in dict.items():
			for link in links:
				found = False
				for tmp_link in files:
					if link[1] == tmp_link[1]:
						found = True
						if not service in tmp_link[2]:
							tmp_link[2].append(service)
							tmp_link[0].append(link[0])
				if not found:
					files.append(([link[0]], link[1], [service], link[2], link[3]))
		while len(files) > 0:
			tmp_name = []
			first = files[0]
			others = files[1:]
			for link in others:
				chars = re.split("[0-9]+", link[1])
				nums = re.split("[^0-9]+", link[1])
				tmp = ""
				for i in chars:
					if tmp+i == first[1][0:len(tmp+i)]:
						tmp += i
						for j in nums:
							if tmp+j == first[1][0:len(tmp+j)]:
								tmp += j
				tmp_name.append(tmp)
			final_name = ""
			for name in tmp_name:
				if len(name) > len(final_name):
					final_name = name
			if len(final_name) > 0:
				packages.append((final_name, [first]))
				del files[files.index(first)]
				tmp_list = []
				for link in files:
					if final_name in link[1]:
						tmp_list.append(link)
				for package_name, package_files in packages:
					if package_name == final_name:
						package_files += tmp_list
				for i in tmp_list:
					del files[files.index(i)]
			else:
				alone_name = first[1]
				alone_name = alone_name.split(".")
				alone_name.pop()
				alone_name = ".".join(alone_name)
				packages.append((alone_name, [first]))
				del files[files.index(first)]
		return packages

if __name__ == "__main__":
	l = PackageManager()
	for package in l.create_packages(LINKS):
		print package