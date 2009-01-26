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
 
NAME=tucan
EXEC=tucan.py
MANPAGE=tucan.1.gz
DOCFILES=CHANGELOG LICENSE README README.es TODO
 
PREFIX=/usr/local
BINDIR=$(PREFIX)/bin/
LIBDIR=$(PREFIX)/lib/tucan/
MANDIR=$(PREFIX)/share/man/man1/
DOCDIR=$(PREFIX)/share/tucan/
 
.PHONY : update install uninstall
 
update:
	svn update
 
install:
	mkdir -p $(BINDIR)
	mkdir -p $(LIBDIR)
	cp -R $(PWD)/* $(LIBDIR)
	chmod 755 $(LIBDIR)$(EXEC)
	ln -s $(LIBDIR)$(EXEC) $(BINDIR)$(NAME)
 
	mkdir -p $(MANDIR)
	install -m 644 $(MANPAGE) $(MANDIR)
 
	mkdir -p $(DOCDIR)
	install -m 644 $(DOCFILES) $(DOCDIR)
 
uninstall:
	rm -r $(DOCDIR)
	rm $(MANDIR)$(MANPAGE)
	rm -r $(LIBDIR)
	rm $(BINDIR)$(NAME)