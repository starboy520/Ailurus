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

class Autostart_Workrave(C):
    __doc__ = _('Automatically start up Workrave\n'
                'Create file ~/.config/autostart/workrave.desktop')
    path = os.path.expanduser('~/.config/autostart/')
    file = path + 'workrave.desktop'
    def exists(self):
        if UBUNTU or MINT:
            return APT.installed('workrave') and not os.path.exists(self.file)
        if FEDORA:
            return RPM.installed('workrave') and not os.path.exists(self.file)
        return False
    def cure(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(self.file, 'w') as f:
            f.write('[Desktop Entry]\n'
                    'Name=Workrave\n'
                    'Exec=workrave\n'
                    'Encoding=UTF-8\n'
                    'Version=1.0\n'
                    'Type=Application\n'
                    'X-GNOME-Autostart-enabled=true\n')

class Create_basic_vimrc(C):
    __doc__ = _('Create basic ~/.vimrc\n'
                'Content: syntax on; set autoindent; set number; set mouse=a')
    file = os.path.expanduser('~/.vimrc')
    def exists(self):
        if UBUNTU or MINT:
            return APT.installed('vim') and not os.path.exists(self.file)
        if FEDORA:
            return RPM.installed('vim-enhanced') and not os.path.exists(self.file)
        return False
    def cure(self):
        with open(self.file, 'w') as f:
            f.write('syntax on\n'
                    'set autoindent\n'
                    'set number\n'
                    'set mouse=a\n')

class Create_Imagemagick_shortcut(C):
    __doc__ = _('Create ImageMagicK shortcut in menu')
    file = '/usr/share/applications/imagemagick.desktop'
    def exists(self):
        if UBUNTU or MINT:
            return APT.installed('imagemagick') and not os.path.exists(self.file)
        if FEDORA:
            return RPM.installed('ImageMagick') and not os.path.exists(self.file)
        return False
    def cure(self):
        path = D + 'umut_icons/imagemagick.png'
        run_as_root('cp %s /usr/share/icons/ ' % path)
        create_file(self.file, '[Desktop Entry]\n'
                               'Name=ImageMagick\n'
                               'Exec=display %f\n'    
                               'Encoding=UTF-8\n'
                               'StartupNotify=true\n'
                               'Terminal=true\n'
                               'Type=Application\n'
                               'Categories=GNOME;GTK;Graphics;\n'
                               'Icon=/usr/share/icons/imagemagick.png\n')

