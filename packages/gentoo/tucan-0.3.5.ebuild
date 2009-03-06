# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $
 
RESTRICT="mirror"
 
DESCRIPTION="download and upload manager for hosting sites"
HOMEPAGE="http://cusl3-tucan.forja.rediris.es/"
SRC_URI="http://forja.rediris.es/frs/download.php/1135/${P}.tar.gz"
 
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
    dodir /usr/share/pixmaps/
    cp -R ${S}/ ${D}/usr/share/${PN}/
    cp ${S}/media/${PN}.svg ${D}/usr/share/pixmaps/${PN}.svg

    # Make the Python script executable
    chmod a+x ${D}/usr/share/${PN}/${PN}.py
 
    # Symlink the Python script into /usr/bin
    dodir /usr/bin/
    dosym /usr/share/${PN}/${PN}.py /usr/bin/${PN}
 
    # Install Man and Doc
    doman ${PN}.1.gz
    dodoc CHANGELOG LICENSE README README.es TODO
}
