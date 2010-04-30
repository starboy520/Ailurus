#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
# Copyright (C) 2009-2010, Ailurus Developers Team
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

class Electric(_path_lists):
    __doc__ = _('Electric: A software for IC design which supports VHDL and Verilog')
    detail = ( _('Official site: <span color="blue"><u>http://www.staticfreesoft.com/</u></span>') +
               _(' This application depends on Java.') )
    category = 'em'
    license = GPL
    def __init__(self):
        self.shortcut = '/usr/share/applications/electric.desktop'
        self.file = '/opt/electricBinary.jar'
        self.paths = [self.shortcut, self.file]
    def install(self):
        f = R(
['http://ftp.gnu.org/pub/gnu/electric/electricBinary-8.09.jar'],
11102701, 'c50557bc54b74948e707dc4606009bd93274ec71').download()

        run_as_root('mkdir /opt', ignore_error=True)
        run_as_root('cp %s %s'%(f, self.file) )
        create_file(self.shortcut, '''[Desktop Entry]
Name=Electric
Exec=java -jar %s -Xms512M -Xmx1024M -Dsun.java2d.opengl=true
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering;'''%self.file)

class QCad(_rpm_install):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    license = GPL
    category = 'em'
    if FEDORA:
        pkgs = 'qcad'

