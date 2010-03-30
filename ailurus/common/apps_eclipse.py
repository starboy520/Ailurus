#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
#
# Ailurus is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ailurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ailurus; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from __future__ import with_statement
import sys, os
from lib import *
from libapp import *

def message(title, content):
    import StringIO
    assert isinstance(title, (str, unicode)) and title
    assert isinstance(content, (str, unicode, StringIO.StringIO) )
    if isinstance(content, StringIO.StringIO): content = content.getvalue()
    
    import gtk
    dialog = gtk.MessageDialog(buttons=gtk.BUTTONS_CLOSE)
    dialog.set_title( _('Installing Eclipse extension') )
    dialog.set_markup('<big><b>%s</b></big>\n\n'%title + content)
    dialog.show_all()
    gtk.gdk.threads_enter()
    dialog.run()
    dialog.destroy()
    gtk.gdk.threads_leave()

class _parser:
    def __init__(self):
        self.attension = False
        self.url = None
    def cope_a(self, line):
        if self.attension == False: return
        if self.url: return
        
        import re
        match = re.search('<a href="([^"]+)"', line)
        assert match
        self.url = match.group(1)
        assert self.url.startswith('download.php?'), self.url
    def cope_download(self, line):
        self.attension = True
    def cope(self, line):
        if '<b>Download</b>' in line:
            self.cope_download(line)
        elif '<a href=' in line:
            self.cope_a(line)
    def parse(self, URL):
        import urllib2
        f = urllib2.urlopen(URL)
        lines = f.readlines()
        f.close()
        for line in lines:
            self.cope(line)
        assert self.url
        return self.url

def create_eclipse_icon():
        memarg = ''
        try:
            f = open('/proc/meminfo')
            for line in f:
                if 'MemTotal' in line:
                    amount = int(line.split()[1]) ; break
            if amount >= 1024 * 1024 * 1.5:
                memarg = '-Xms512M -Xmx1024M'
        except:
            pass
        icon = '/usr/share/applications/eclipse.desktop'
        with TempOwn(icon) as o:
            with open(icon, 'w') as f:
                f.write('''[Desktop Entry]
Name=Eclipse
Exec=sh -c "export GDK_NATIVE_WINDOWS=true; exec /opt/eclipse/eclipse -vmargs ''' + memarg + ''' -Dsun.java2d.opengl=true"
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Development
Icon=/opt/eclipse/icon.xpm''')

class Eclipse_basic(_path_lists):
        
    __doc__ = _('Eclipse (basic development environment)')
    detail = ( 
            _('Eclipse is from http://www.eclipse.org/downloads/ \n') +
            _('You can install Language pack according to the instructions on the page http://www.eclipse.org/babel/downloads.php\n'
              'You can download Language pack from http://download.eclipse.org/technology/babel/babel_language_packs/ganymede.php, '
              'and extract ".zip" file to directory "/opt/eclipse" .') + 
            _(' This application depends on Java.') )
    category = 'eclipse'
    logo = 'eclipse.png'
    license = ('Eclipse Public License (EPL), '
               'see http://www.eclipse.org/org/documents/epl-v10.php')
        
    def install(self):
        if get_arch() == 32:
            r = R([
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.cdpa.nsysu.edu.tw/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.jaist.ac.jp/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.yz.yamagata-u.ac.jp/pub/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://www.ring.gr.jp/pub/misc/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.in.th/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.korea.ac.kr/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirrors.nsa.co.il/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.stu.edu.tw/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://kambing.ui.ac.id/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.kaist.ac.kr/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.cs.pu.edu.tw/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.stu.edu.tw/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.daum.net/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.cs.pu.edu.tw/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.daum.net/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirror.in.th/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.kaist.ac.kr/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.jaist.ac.jp/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirrors.nsa.co.il/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.stu.edu.tw/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.unixheads.org/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.ussg.iu.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.csclub.uwaterloo.ca/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.cs.rit.edu/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://www.gtlib.gatech.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.cse.buffalo.edu/pub/Eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirrors.med.harvard.edu/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirror.cc.columbia.edu/pub/software/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.ussg.iu.edu/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.osuosl.org/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.unixheads.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.cc.vt.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirrors.xmission.com/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirror.cc.vt.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirror.csclub.uwaterloo.ca/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirrors.ibiblio.org/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://carroll.aset.psu.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.cc.columbia.edu/pub/software/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://carroll.aset.psu.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirrors.xmission.com/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.mirrors.tds.net/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirrors.ibiblio.org/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.selfnet.de/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.a3-system.be/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.man.szczecin.pl/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.roedu.net/mirrors/eclipse.org//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirror.netcologne.de/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.cc.uoc.gr/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.rnl.ist.utl.pt/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.roedu.net/pub/mirrors/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.switch.ch/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.roedu.net/pub/mirrors/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://www.rcp-vision.com/pub/eclipse/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.ing.umu.se/mirror/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.ialto.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.rnl.ist.utl.pt/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.dcc.fc.up.pt/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://sunsite.informatik.rwth-aachen.de/pub/mirror/eclipse/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.saplabs.bg/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirror.selfnet.de/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.roedu.net/mirrors/eclipse.org//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.mirror.kangaroot.net/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://rm.mirror.garr.it/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.cc.uoc.gr/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://mirrors.linux-bg.org/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.netcologne.de/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.ulak.net.tr/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.ialto.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.saplabs.bg//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://sunsite.informatik.rwth-aachen.de/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://rm.mirror.garr.it/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.heanet.ie/pub/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirror.kreksi.net/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.sh.cvut.cz/MIRRORS/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipsemirror.yoxos.com/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.heanet.ie/pub/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.mirror.kangaroot.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://www.eclipse.ps.pl/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.i-logic.hu//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://mirrors.linux-bg.org/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://filemirror.hu/pub/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.ulak.net.tr/eclipse/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.man.poznan.pl/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://www.rcp-vision.com/eclipse/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.sh.cvut.cz/MIRRORS/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.ing.umu.se/mirror/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.man.poznan.pl/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://ftp.saix.net/Eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://eclipse.c3sl.ufpr.br/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://eclipse.c3sl.ufpr.br/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'ftp://ftp.pucpr.br/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
'http://linorg.usp.br/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk.tar.gz',
                   ])
        else:
            r = R([
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.daum.net/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.jaist.ac.jp/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.in.th/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://kambing.ui.ac.id/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.yz.yamagata-u.ac.jp/pub/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirrors.nsa.co.il/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.kaist.ac.kr/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.cdpa.nsysu.edu.tw/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.cs.pu.edu.tw/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.korea.ac.kr/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.stu.edu.tw/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://www.ring.gr.jp/pub/misc/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.stu.edu.tw/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.daum.net/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.jaist.ac.jp/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.nsa.co.il/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.stu.edu.tw/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.in.th/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.kaist.ac.kr/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.cse.buffalo.edu/pub/Eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirrors.ibiblio.org/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.cc.vt.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.cs.rit.edu/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.cc.columbia.edu/pub/software/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.osuosl.org/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.cc.vt.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirrors.xmission.com/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.csclub.uwaterloo.ca/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://carroll.aset.psu.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.unixheads.org/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.csclub.uwaterloo.ca/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ussg.iu.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirrors.med.harvard.edu/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.unixheads.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.cc.columbia.edu/pub/software/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.ussg.iu.edu/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.xmission.com/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.ibiblio.org/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.mirrors.tds.net/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://www.gtlib.gatech.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://carroll.aset.psu.edu/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.ulak.net.tr/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.ialto.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.switch.ch/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipsemirror.yoxos.com/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://sunsite.informatik.rwth-aachen.de/pub/mirror/eclipse/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.saplabs.bg/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.man.szczecin.pl/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.sh.cvut.cz/MIRRORS/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.ialto.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.roedu.net/mirrors/eclipse.org//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.heanet.ie/pub/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.linux-bg.org/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.heanet.ie/pub/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://www.rcp-vision.com/pub/eclipse/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.man.poznan.pl/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.netcologne.de/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.roedu.net/pub/mirrors/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.mirror.kangaroot.net/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.a3-system.be/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.kreksi.net/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.dcc.fc.up.pt/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://sunsite.informatik.rwth-aachen.de/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://www.eclipse.ps.pl/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ulak.net.tr/eclipse/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.man.poznan.pl/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://www.rcp-vision.com/eclipse/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ing.umu.se/mirror/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.i-logic.hu//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.ing.umu.se/mirror/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://rm.mirror.garr.it/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.netcologne.de/eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirrors.linux-bg.org/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.cc.uoc.gr/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.rnl.ist.utl.pt/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.rnl.ist.utl.pt/pub/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://rm.mirror.garr.it/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://mirror.selfnet.de/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.roedu.net/mirrors/eclipse.org//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://filemirror.hu/pub/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.selfnet.de/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.cc.uoc.gr/mirrors/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.sh.cvut.cz/MIRRORS/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.saplabs.bg//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.roedu.net/pub/mirrors/eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.mirror.kangaroot.net/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://ftp.saix.net/Eclipse//eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://eclipse.c3sl.ufpr.br/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'http://linorg.usp.br/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.pucpr.br/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.c3sl.ufpr.br/eclipse/eclipse/downloads/drops/R-3.5.1-200909170800/eclipse-SDK-3.5.1-linux-gtk-x86_64.tar.gz',
                   ])
        f = r.download()
        import os
        if not os.path.exists('/opt'): gksudo('mkdir /opt')
        FileServer.chdir('/opt')
        try:
            gksudo("rm eclipse -rf")
            gksudo("tar xzf %s"%f)
            gksudo("chown $USER:$USER eclipse -R")
        finally:
            FileServer.chdir_back()
        
        create_eclipse_icon()
    def __init__(self):
        self.paths = [ '/opt/eclipse', '/usr/share/applications/eclipse.desktop' ]
    @classmethod
    def make_sure_installed(cls):
        obj = cls()
        if not obj.installed(): obj.install()
        
    def remove(self):
        import lib
        import os
        if os.path.isdir('/opt/eclipse/'): 
            gksudo('rm /opt/eclipse/ -rf')
        elif APT.installed('eclipse'):
            APT.remove('eclipse-platform')

    def installed(self):
        import lib
        import os
        if os.path.isdir('/opt/eclipse/') or APT.installed('eclipse'):
            return True
        else:
            return False
        
        
class Eclipse_J2EE(_path_lists):
    __doc__ = _('Eclipse (basic development environment + J2EE)')
    category = 'eclipse'
    logo = 'eclipse.png'
    license = ('Eclipse Public License (EPL), '
               'see http://www.eclipse.org/org/documents/epl-v10.php')
    def install(self):
        if get_arch() == 32:
            r = R([
'http://download.actuatechina.com/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.stu.edu.tw/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.daum.net/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.kaist.ac.kr/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirrors.nsa.co.il/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.stu.edu.tw/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.cs.pu.edu.tw/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.yz.yamagata-u.ac.jp/pub/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirrors.nsa.co.il/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://kambing.ui.ac.id/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.kaist.ac.kr/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.in.th/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.daum.net/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.stu.edu.tw/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirrors.ibiblio.org/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.cc.columbia.edu/pub/software/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://carroll.aset.psu.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.csclub.uwaterloo.ca/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.unixheads.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirrors.ibiblio.org/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirrors.med.harvard.edu/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.osuosl.org/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.cc.vt.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.ussg.iu.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://carroll.aset.psu.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.cs.rit.edu/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://www.gtlib.gatech.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.cc.columbia.edu/pub/software/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.cc.vt.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.unixheads.org/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirrors.xmission.com/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.ussg.iu.edu/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.cse.buffalo.edu/pub/Eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirrors.xmission.com/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.csclub.uwaterloo.ca/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://www.rcp-vision.com/pub/eclipse/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.man.poznan.pl/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.netcologne.de/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.ntua.gr/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.roedu.net/mirrors/eclipse.org//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.i-logic.hu//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.switch.ch/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.roedu.net/mirrors/eclipse.org//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.man.szczecin.pl/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://rm.mirror.garr.it/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://rm.mirror.garr.it/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.ing.umu.se/mirror/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.ing.umu.se/mirror/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.mirror.kangaroot.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.roedu.net/pub/mirrors/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://www.rcp-vision.com/eclipse/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.heanet.ie/pub/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.netcologne.de/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.cc.uoc.gr/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.man.poznan.pl/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.ulak.net.tr/eclipse/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.a3-system.be/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirrors.linux-bg.org/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.roedu.net/pub/mirrors/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.ialto.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.switch.ch/mirror/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.ulak.net.tr/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.saplabs.bg/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.ialto.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.ntua.gr/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirrors.linux-bg.org/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.saplabs.bg//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://mirror.selfnet.de/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.heanet.ie/pub/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipsemirror.yoxos.com/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.mirror.kangaroot.net/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.sh.cvut.cz/MIRRORS/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.cc.uoc.gr/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://mirror.selfnet.de/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.inescn.pt/pub/util/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://ftp.sh.cvut.cz/MIRRORS/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://linorg.usp.br/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'ftp://eclipse.c3sl.ufpr.br/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://eclipse.c3sl.ufpr.br/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
'http://espelhos.edugraf.ufsc.br/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk.tar.gz',
                   ])
        else:
            r = R([
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://download.actuatechina.com/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.cs.pu.edu.tw/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.kaist.ac.kr/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.stu.edu.tw/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.daum.net/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.stu.edu.tw/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirrors.nsa.co.il/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.yz.yamagata-u.ac.jp/pub/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.kaist.ac.kr/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.in.th/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.daum.net/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.stu.edu.tw/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.nsa.co.il/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://kambing.ui.ac.id/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://carroll.aset.psu.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.ibiblio.org/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirrors.ibiblio.org/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://www.gtlib.gatech.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.unixheads.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.xmission.com/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirrors.xmission.com/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.osuosl.org/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.cc.vt.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.cc.columbia.edu/pub/software/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.cse.buffalo.edu/pub/Eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ussg.iu.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.cc.vt.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirrors.med.harvard.edu/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.cc.columbia.edu/pub/software/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.cs.rit.edu/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://carroll.aset.psu.edu/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.ussg.iu.edu/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.csclub.uwaterloo.ca/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.csclub.uwaterloo.ca/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.unixheads.org/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.man.poznan.pl/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.sh.cvut.cz/MIRRORS/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirrors.linux-bg.org/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.man.poznan.pl/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.ing.umu.se/mirror/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.heanet.ie/pub/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.man.szczecin.pl/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.cc.uoc.gr/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.ialto.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://www.rcp-vision.com/eclipse/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.roedu.net/pub/mirrors/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.ntua.gr/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.ialto.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipsemirror.yoxos.com/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.a3-system.be/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.i-logic.hu//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://rm.mirror.garr.it/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ing.umu.se/mirror/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.saplabs.bg/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.switch.ch/mirror/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.wh2.tu-dresden.de/pub/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.roedu.net/mirrors/eclipse.org//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp.roedu.net/pub/mirrors/eclipse.org/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.sh.cvut.cz/MIRRORS/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.cc.uoc.gr/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.heanet.ie/pub/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.netcologne.de/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ulak.net.tr/eclipse/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://rm.mirror.garr.it/mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.selfnet.de/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://d2u376ub0heus3.cloudfront.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.roedu.net/mirrors/eclipse.org//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.mirror.kangaroot.net/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.saplabs.bg//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.mirror.kangaroot.net/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.ulak.net.tr/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.netcologne.de/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirror.switch.ch/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://mirrors.linux-bg.org/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://mirror.selfnet.de/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.inescn.pt/pub/util/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://www.rcp-vision.com/pub/eclipse/eclipseMirror/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://ftp.ntua.gr/pub/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'ftp://eclipse.c3sl.ufpr.br/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://linorg.usp.br/eclipse/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://espelhos.edugraf.ufsc.br/eclipse//technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
'http://eclipse.c3sl.ufpr.br/technology/epp/downloads/release/galileo/SR1/eclipse-jee-galileo-SR1-linux-gtk-x86_64.tar.gz',
                   ])
        f = r.download()
        import os
        if not os.path.exists('/opt'): gksudo('mkdir /opt')
        FileServer.chdir('/opt')
        try:
            gksudo("rm eclipse -rf")
            gksudo("tar xzf %s"%f)
            gksudo("chown $USER:$USER eclipse -R")
        finally:
            FileServer.chdir_back()
        
        create_eclipse_icon()
    def __init__(self):
        self.paths = [ '/opt/eclipse', '/usr/share/applications/eclipse.desktop' ]
    def installed(self):
        import glob
        List = glob.glob('/opt/eclipse/plugins/org.eclipse.epp.*')
        if bool(List) == False: return False
        return _path_lists.installed(self)

class CDT(_path_lists):
    __doc__ = _('CDT: C/C++ development')
    detail = _('CDT is from http://www.eclipse.org/cdt/')
    category = 'eclipse'
    license = ('Eclipse Public License (EPL), '
               'see http://www.eclipse.org/legal/')
    def __init__(self):
        self.r = R(
['http://tdt.sjtu.edu.cn/S/Eclipse/cdt-master-6.0.0.zip',
'http://download.eclipse.org/tools/cdt/releases/galileo/dist/cdt-master-6.0.0.zip'],
45462495, '9f810b3d4a5cfc7bbbd7deddeceef705be4654a9')
        import os
        import lib
        if APT.installed('eclipse'):
            self.path = '/usr/lib/eclipse/dropins/' + os.path.splitext(self.r.filename)[0]
        else:
            self.path = '/opt/eclipse/dropins/' + os.path.splitext(self.r.filename)[0]
        self.paths = [ self.path ]
    def install(self):
        import os
        Eclipse_basic.make_sure_installed()
        f = self.r.download()
        gksudo('mkdir -p '+self.path)
        gksudo("unzip -qo %s -d %s"%(f, self.path))
        if APT.installed('eclipse'):
            gksudo("chown $USER:$USER /usr/lib/eclipse -R")
        else:
            gksudo("chown $USER:$USER /opt/eclipse -R")

class Pydev(_path_lists):
    __doc__ = _('Pydev: Python development')
    detail = _('Pydev is from http://pydev.org/download.html')
    category = 'eclipse'
    license = ('Eclipse Public License (EPL), '
               'see http://pydev.org/about.html')
    def __init__(self):
        self.r = R(
['http://tdt.sjtu.edu.cn/S/Eclipse/org.python.pydev.feature-1.4.6.2788.zip',
'http://ncu.dl.sourceforge.net/project/pydev/pydev/Pydev%201.4.6/org.python.pydev.feature-1.4.6.2788.zip'],
4765497, '238037546162bf5ee198b5167cc5a32b95a6ab5c')
        import os
        import lib
        if APT.installed('eclipse'):
            self.path = '/usr/lib/eclipse/dropins/' + os.path.splitext(self.r.filename)[0]
        else:
            self.path = '/opt/eclipse/dropins/' + os.path.splitext(self.r.filename)[0]
        self.paths = [ self.path ]
    def install(self):
        import lib
        Eclipse_basic.make_sure_installed()
        f = self.r.download()
        gksudo('mkdir -p '+self.path)
        gksudo("unzip -qo %s -d %s"%(f, self.path))
        if APT.installed('eclipse'):
            gksudo("chown $USER:$USER /usr/lib/eclipse -R")
        else:
            gksudo("chown $USER:$USER /opt/eclipse -R")

class Aptana:
    __doc__ = _('Aptana: Web application development')
    detail = _('Aptana is from http://www.aptana.org/studio/plugin\n'
               'Aptana is installed by http://download.aptana.org/tools/studio/plugin/install/studio\n'
               'Due to limitation of the authors\' programming ability, '
               'Aptana cannot be removed by Ailurus. '
               'In order to remove Aptana, you have to re-install Eclipse.')
    category = 'eclipse'
    license = 'dual-licensed under the terms of Aptana Public License and GPL'
    def installed(self):
        import glob
        import lib
        if APT.installed('eclipse'):
            List = glob.glob('/usr/lib/eclipse/plugins/com.aptana.ide.*')
        else:
            List = glob.glob('/opt/eclipse/plugins/com.aptana.ide.*') 
        return bool(List)
    def install(self):
        Eclipse_basic.make_sure_installed()
        import StringIO
        msg = StringIO.StringIO()
        print >>msg, _('Please launch Eclipse, and go to "Help" -> "Install New Software".')
        print >>msg
        print >>msg, _('Click the "Add" button. Then type <b>%s</b> in "Location".')%'http://download.aptana.org/tools/studio/plugin/install/studio'
        print >>msg
        print >>msg, _('Then click the "Next" button and agree the license.')
        message( _('Installing Aptana'), msg )
    def remove(self):
        raise NotImplementedError

class RadRails:
    __doc__ = _('RadRails: Ruby development')
    detail = _('Over the past RadRails was called "RDT". '
               'RadRails is installed by http://download.aptana.com/tools/radrails/plugin/install/radrails-bundle')
    category = 'eclipse'
    license = 'It is released under GPL v3 and Aptana Public License.'
    def installed(self):
        import glob
        import lib
        if APT.installed('eclipse'):
            List = glob.glob('/usr/share/eclipse/plugins/com.aptana.radrails.*')
        else:
            List = glob.glob('/opt/eclipse/plugins/com.aptana.radrails.*')
        return bool(List)
    def install(self):
        Eclipse_basic.make_sure_installed()
        import StringIO
        msg = StringIO.StringIO()
        print >>msg, _('Please launch Eclipse, and go to "Help" -> "Install New Software".')
        print >>msg
        print >>msg, _('Click the "Add" button. Then type <b>%s</b> in "Location".')%'http://download.aptana.com/tools/radrails/plugin/install/radrails-bundle'
        print >>msg
        print >>msg, _('Then click the "Next" button and agree the license.')
        message( _('Installing RadRails\n'), msg )
    def remove(self):
        raise NotImplementedError

class Mylyn(_path_lists):
    'Mylyn'
    detail = _('Mylyn is from http://www.eclipse.org/mylyn/downloads/')
    category = 'eclipse'
    license = ('Eclipse Public License (EPL), '
               'see http://www.eclipse.org/legal/')
    
    def __init__(self):
        import lib
        if APT.installed('eclipse'):
            self.path = '/usr/share/eclipse/dropins/mylyn'
        else:
            self.path = '/opt/eclipse/dropins/mylyn'
        self.paths = [ self.path ]
    def install(self):
        import lib
        Eclipse_basic.make_sure_installed()
        f = R('http://download.eclipse.org/tools/mylyn/update/mylyn-3.3.1-e3.4.zip').download()
        gksudo('mkdir -p '+self.path)
        gksudo("unzip -qo %s -d %s" % (f, self.path) )
        if APT.installed('eclipse'):
            gksudo("chown $USER:$USER /usr/lib/eclipse -R")
        else:
            gksudo("chown $USER:$USER /opt/eclipse -R")

class DLTK:
    __doc__ = _('Dynamic languages toolkit')
    detail = _('It is installed by http://download.eclipse.org/technology/dltk/updates-dev/2.0/')
    category = 'eclipse'
    License = ('Eclipse Distribution License (EDL), Eclipse Public License (EPL), '
               'see http://www.eclipse.org/legal/')
    def installed(self):
        import glob
        List = glob.glob('/opt/eclipse/plugins/org.eclipse.dltk.*')
        return bool(List)
    def install(self):
        Eclipse_basic.make_sure_installed()
        import StringIO
        msg = StringIO.StringIO()
        print >>msg, _('Please launch Eclipse, and go to "Help" -> "Install New Software".')
        print >>msg
        print >>msg, _('Click the "Add" button. Then type <b>%s</b> in "Location".')%'http://download.eclipse.org/technology/dltk/updates-dev/2.0/'
        print >>msg
        print >>msg, _('Then click the "Next" button and agree the license.')
        message( _('Installing Dynamic languages toolkit\n'), msg )
    def remove(self):
        raise NotImplementedError
    @classmethod
    def make_sure_installed(cls):
        obj = cls()
        if not obj.installed(): obj.install()

class PDT:
    __doc__ = _('PDT: PHP development')
    detail = _('PDT is from http://www.eclipse.org/pdt/downloads/')
    category = 'eclipse'
    license = ('Eclipse Public License (EPL), '
               'see http://www.eclipse.org/legal/')
    def installed(self):
        import glob
        import lib
        if APT.installed('eclipse'):
            List = glob.glob('/usr/lib/eclipse/plugins/org.eclipse.php.*')
        else:
            List = glob.glob('/opt/eclipse/plugins/org.eclipse.php.*')
        return bool(List)
    def install(self):
        DLTK.make_sure_installed()
        import StringIO
        msg = StringIO.StringIO()
        print >>msg, _('Please launch Eclipse, and go to "Help" -> "Install New Software".')
        print >>msg
        print >>msg, _('Click the "Add" button. Then type <b>%s</b> in "Location".')%'http://www.eclipse.org/pdt/downloads/'
        print >>msg
        print >>msg, _('Then click the "Next" button and agree the license.')
        message( _('Installing PDT\n'), msg )
    def remove(self):
        raise NotImplementedError

class Subversive:
    __doc__ = _('Subversive: Use SVN in Eclipse')
    detail = _('It is installed by http://download.eclipse.org/technology/subversive/0.7/update-site/')
    category = 'eclipse'
    license = 'Eclipse Public License (EPL)'
    def installed(self):
        import glob
        import lib
        if APT.installed('eclipse'):
            List = glob.glob('/usr/lib/eclipse/plugins/org.eclipse.team.svn.*')
        else:
            List = glob.glob('/opt/eclipse/plugins/org.eclipse.team.svn.*')            
        return bool(List)
    def install(self):
        Eclipse_basic.make_sure_installed()
        import StringIO
        msg = StringIO.StringIO()
        print >>msg, _('Please launch Eclipse, and go to "Help" -> "Install New Software".')
        print >>msg
        print >>msg, _('Click the "Add" button. Then type <b>%s</b> in "Location".')%'http://download.eclipse.org/technology/subversive/0.7/update-site/'
        print >>msg
        print >>msg, _('Then click the "Next" button and agree the license.')
        message( _('Installing Subversive\n'), msg )
    def remove(self):
        raise NotImplementedError

class MTJ(_path_lists):
    __doc__ = _('MTJ: J2ME development')
    detail = _('It is downloaded from http://download.eclipse.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/')
    category = 'eclipse'
    license = 'Eclipse Public License (EPL), GNU General Public License (GPL)'
    def __init__(self):
        import lib
        if APT.installed('eclipse'):
            self.path = '/opt/eclipse/dropins/MTJ/'
        else:
            self.path = '/usr/lib/eclipse/dropins/MTJ/'
        self.paths = [ self.path ]
    def install(self):
        Eclipse_basic.make_sure_installed()
        r = R([
'http://d2u376ub0heus3.cloudfront.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirrors.nsa.co.il/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://d2u376ub0heus3.cloudfront.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.in.th/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.kaist.ac.kr/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.cs.pu.edu.tw/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://kambing.ui.ac.id/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.stu.edu.tw/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.yz.yamagata-u.ac.jp/pub/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.stu.edu.tw/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.daum.net/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://d2u376ub0heus3.cloudfront.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.jaist.ac.jp/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.jaist.ac.jp/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.daum.net/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.kaist.ac.kr/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.stu.edu.tw/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirrors.nsa.co.il/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.in.th/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://kambing.ui.ac.id/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirrors.ibiblio.org/pub/mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.cse.buffalo.edu/pub/Eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://www.gtlib.gatech.edu/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.ussg.iu.edu/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://d2u376ub0heus3.cloudfront.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.cc.vt.edu/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirrors.xmission.com/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://carroll.aset.psu.edu/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.cs.rit.edu/mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.cc.vt.edu/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.cc.columbia.edu/pub/software/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.ussg.iu.edu/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.csclub.uwaterloo.ca/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirrors.xmission.com/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.cc.columbia.edu/pub/software/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.csclub.uwaterloo.ca/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirrors.med.harvard.edu/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.mirrors.tds.net/pub/eclipse.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://carroll.aset.psu.edu/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.osuosl.org/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.roedu.net/pub/mirrors/eclipse.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.cc.uoc.gr/mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.heanet.ie/pub/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.ialto.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.man.poznan.pl/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp-stud.fht-esslingen.de/pub/Mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.ing.umu.se/mirror/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://www.rcp-vision.com/pub/eclipse/eclipseMirror/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.switch.ch/mirror/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://rm.mirror.garr.it/mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.ialto.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://d2u376ub0heus3.cloudfront.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://www.rcp-vision.com/eclipse/eclipseMirror/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.sh.cvut.cz/MIRRORS/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipsemirror.yoxos.com/eclipse.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://rm.mirror.garr.it/mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.a3-system.be/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.selfnet.de/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirrors.linux-bg.org/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.man.szczecin.pl/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.roedu.net/mirrors/eclipse.org//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.man.poznan.pl/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.i-logic.hu//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.mirror.kangaroot.net/pub/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.selfnet.de/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://d2u376ub0heus3.cloudfront.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.mirror.kangaroot.net/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.sh.cvut.cz/MIRRORS/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.saplabs.bg/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.heanet.ie/pub/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirror.netcologne.de/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.cc.uoc.gr/mirrors/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.roedu.net/mirrors/eclipse.org//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://mirror.netcologne.de/eclipse//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.ulak.net.tr/eclipseMirror/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://mirrors.linux-bg.org/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.ing.umu.se/mirror/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://ftp.roedu.net/pub/mirrors/eclipse.org/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.saplabs.bg//dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://ftp.ulak.net.tr/eclipse/eclipseMirror/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://linorg.usp.br/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'ftp://eclipse.c3sl.ufpr.br/eclipse/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
'http://eclipse.c3sl.ufpr.br/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip',
               ])
        f = r.download()
        gksudo('mkdir -p '+self.path)
        gksudo("unzip -qo %s -d %s"%(f, self.path))
        if APT.installed('eclipse'):
            gksudo("chown $USER:$USER /usr/share/eclipse -R")
        else:
            gksudo("chown $USER:$USER /opt/eclipse -R")
