###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crakotaku(at)yahoo.es
## Copyright (C) 2008-2009 Paco Salido beakman(at)riseup.net
## Copyright (C) 2008-2009 JM Cordero betic0(at)gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
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

MANDIR=/usr/local/share/man/man1/
LIBDIR=/usr/local/lib/tucan/
BINDIR=/usr/local/bin/
MAN=tucan.1.gz
SRC=tucan.py
NAME=tucan

.PHONY : update install uninstall

update:
	svn update
	
install:
	mkdir -p $(LIBDIR)
	cp -R $(PWD) $(LIBDIR)
	chmod 755 $(LIBDIR)$(SRC)
	ln -s $(LIBDIR)$(SRC) $(BINDIR)$(NAME)
	mkdir -p $(MANDIR)
	cp $(LIBDIR)$(MAN) $(MANDIR)
	chmod 644 $(MANDIR)$(MAN)
	
uninstall:
	rm -r $(LIBDIR)
	rm $(BINDIR)$(NAME)
	rm $(MANDIR)$(MAN)