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
MAINDIR		=	$(DESTDIR)/share/tucan/
ICONDIR		=	$(DESTDIR)/share/pixmaps/
MANDIR		=	$(DESTDIR)/share/man/man1/
DESKTOPDIR	=	$(DESTDIR)/share/applications/
 
NAME		=	tucan
EXECFILE	=	tucan.py
ICONFILE	=	tucan.svg
MANPAGE		=	tucan.1.gz
DESKTOPFILE	=	tucan.desktop
PLUGINDIR	=	default_plugins/
I18NDIR		=	i18n/
MEDIADIR	=	media/
 
basic-install:
	mkdir -p $(BINDIR) $(MAINDIR) $(ICONDIR) $(MANDIR) $(DESKTOPDIR)
 
	install -m 644 *.py $(MAINDIR)
	chmod 755 $(MAINDIR)$(EXECFILE)
 
	cp -R $(PLUGINDIR) $(MAINDIR)$(PLUGINDIR)
	cp -R $(I18NDIR) $(MAINDIR)$(I18NDIR)
	cp -R $(MEDIADIR) $(MAINDIR)$(MEDIADIR)
 
	install -m 644 $(MEDIADIR)$(ICONFILE) $(ICONDIR)
 
	install -m 644 $(MANPAGE) $(MANDIR)
 
	install -m 644 $(DESKTOPFILE) $(DESKTOPDIR)
 
install:
	make basic-install
 
	ln -sf $(MAINDIR)$(EXECFILE) $(BINDIR)$(NAME)
 
uninstall:
	rm -rf $(MAINDIR)
	rm -f $(BINDIR)$(NAME)
	rm -f $(ICONDIR)$(ICONFILE)
	rm -f $(MANDIR)$(MANPAGE)
	rm -f $(DESKTOPDIR)$(DESKTOPFILE)