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

class OpenJUMP(_path_lists):
    __doc__ = _('OpenJUMP: A geographic information system')
    detail = ( 
              _('Official site: http://openjump.org/ .') +
              _(' This application depends on Java.') )
    license = GPL
    category = 'geography'
    license = GPL
    def __init__(self):
        self.shortcut = '/usr/share/applications/openjump.desktop'
        self.dir = '/opt/openjump-1.3'
        self.paths = [self.shortcut, self.dir]
    def install(self):
        f = R(
['http://ncu.dl.sourceforge.net/project/jump-pilot/OpenJUMP/1.3/openjump-v1.3.zip'],
12431980, '4df9363f0e41c797f99265107d57184b8c394ae8').download()

        with Chdir('/tmp') as o:
            run('unzip -oq %s'%f)
            import os
            if not os.path.exists('/opt'):
                run_as_root('mkdir /opt')
            if not os.path.exists(self.dir):
                run_as_root('mv openjump-1.3 /opt/')
            create_file(self.shortcut, '''[Desktop Entry]
Name=OpenJUMP
Exec=bash /opt/openjump-1.3/bin/openjump.sh
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering; ''')

