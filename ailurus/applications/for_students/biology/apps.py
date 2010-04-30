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

class Bioclipse(_path_lists):
    __doc__ = _('Bioclipse: an awesome Chemical and Biological Informatics application')
    detail = _('It is from http://sourceforge.net/projects/bioclipse/files/bioclipse2/')
    category = 'biology'
    license = ('Eclipse Public License (EPL) + exception, '
               'see http://www.bioclipse.net/license-0')
    def __init__(self):
        self.shortcut = '/usr/share/applications/bioclipse.desktop'
        self.path = '/opt/bioclipse'
        self.paths = [ self.shortcut, self.path ]
    def install(self):
        if get_arch() == 32:
            f = R(['http://sourceforge.net/projects/bioclipse/files/bioclipse2/bioclipse2.0/bioclipse2.0.linux.gtk.x86.zip/download'],
                  filename = 'bioclipse2.0.linux.gtk.x86.zip').download()
        else:
            f = R(['http://sourceforge.net/projects/bioclipse/files/bioclipse2/bioclipse2.0/bioclipse2.0.linux.gtk.x86_64.zip/download'],
                  filename = 'bioclipse2.0.linux.gtk.x86_64.zip').download()
        with Chdir('/tmp') as o:
            run('unzip -qo %s' %f)
            import os
            if not os.path.exists('/opt'): run_as_root('mkdir /opt')
            run_as_root('rm /opt/bioclipse -rf')
            if get_arch() == 32:
                run_as_root('mv bioclipse2.0.linux.gtk.x86/bioclipse /opt/')
            else:
                run_as_root('mv bioclipse2.0.linux.gtk.x86_64/bioclipse /opt/')
            run_as_root('chown $USER:$USER /opt/bioclipse -R')
            
            create_file(self.shortcut,'''[Desktop Entry]
Name=Bioclipse
Exec=/opt/bioclipse/bioclipse
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Development
Icon=/opt/bioclipse/icon.xpm 
''')
            
            file_append('/opt/bioclipse/bioclipse.ini', '-Dorg.eclipse.swt.browser.XULRunnerPath=/usr/lib/xulrunner/')

