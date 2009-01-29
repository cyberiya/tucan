# paste /usr/local/portage/www-apps/tucan/tucan-0.3.2.ebuild
# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $
 
RESTRICT="mirror"
 
DESCRIPTION="download and upload manager for hosting sites"
HOMEPAGE="http://cusl3-tucan.forja.rediris.es/"
SRC_URI="http://forja.rediris.es/frs/download.php/1079/${P}.tar.gz"
 
LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64 ~x86"  
IUSE=""
 
DEPEND="app-text/tesseract[tiff,linguas_en]
        dev-lang/python
        dev-python/imaging
        dev-python/pygtk
        gnome-base/librsvg"
 
RDEPEND="${DEPEND}"
 
src_unpack() {
    if [ "${A}" != "" ]; then
	    unpack ${A}
    fi
}
 
src_compile() {
    einfo "Nothing to compile"
}
 
src_install() {
    # Install Python script, modules, and other supporting stuff
    dodir /usr/share/
    cp -R ${S}/ ${D}/usr/share/tucan/
 
    # Make the Python script executable
    chmod a+x ${D}/usr/share/tucan/tucan.py
 
    # Symlink the Python script into /usr/bin
    dodir /usr/bin/
    dosym /usr/share/tucan/tucan.py /usr/bin/tucan
 
    # Install Man and Doc
    doman tucan.1.gz
    dodoc CHANGELOG LICENSE README README.es TODO
}
