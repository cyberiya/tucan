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
 
DESTDIR		=	/usr/local
BINDIR		=	$(DESTDIR)/bin/
LIBDIR		=	$(DESTDIR)/lib/tucan/
DOCDIR		=	$(DESTDIR)/share/tucan/
MANDIR		=	$(DESTDIR)/share/man/man1/
ICONDIR		=	$(DESTDIR)/share/pixmaps/
DESKTOPDIR	=	$(DESTDIR)/share/applications/
 
NAME		=	tucan
EXECFILE	=	tucan.py
MANPAGE		=	tucan.1.gz
ICONFILE	=	tucan.svg
DESKTOPFILE	=	tucan.desktop
DOCFILES	=	CHANGELOG LICENSE README README.es TODO
PLUGINDIR	=	default_plugins/
I18NDIR		=	i18n/
MEDIADIR	=	media/
 
install:
	mkdir -p $(BINDIR) $(LIBDIR) $(DOCDIR) $(MANDIR) $(ICONDIR) $(DESKTOPDIR)
 
	install -m 644 *.py $(LIBDIR)
	chmod 755 $(LIBDIR)$(EXECFILE)
	ln -s $(LIBDIR)$(EXECFILE) $(BINDIR)$(NAME)
 
	cp -R $(PLUGINDIR) $(LIBDIR)$(PLUGINDIR)
	cp -R $(I18NDIR) $(LIBDIR)$(I18NDIR)
	cp -R $(MEDIADIR) $(LIBDIR)$(MEDIADIR)
 
	install -m 644 $(DOCFILES) $(DOCDIR)
 
	install -m 644 $(MANPAGE) $(MANDIR)
 
	install -m 644 $(MEDIADIR)$(ICONFILE) $(ICONDIR)
 
	install -m 644 $(DESKTOPFILE) $(DESKTOPDIR)
 
uninstall:
	rm -r $(LIBDIR) $(DOCDIR)
	rm $(BINDIR)$(NAME)
	rm $(MANDIR)$(MANPAGE)
	rm $(ICONDIR)$(ICONFILE)
	rm $(DESKTOPDIR)$(DESKTOPFILE)