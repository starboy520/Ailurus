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

class Colorful_BASH_prompt_symbols(C):
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = (_('Add this line into ~/.bashrc:') + '\n' + 
              r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '")
    bashrc = os.path.expanduser('~/.bashrc')
    line = r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '"
    def exists(self):
        return not file_contain(self.bashrc, self.line)
    def cure(self):
        file_append(self.bashrc, self.line)
        notify( _('The color of bash prompt symbols is changed.'), _('It will take effect at the next time you log in.') )

class Fix_error_in_49_sansserif_conf(C):
    __doc__ = _('Fix errors in 49-sansserif.conf. Otherwise, some character in Flash would be displayed as blank diamond.')
    detail = _('Change "sans-serif" to "sans serif".')
    type = C.MUST_FIX
    def exists(self):
        try:
            with open('/etc/fonts/conf.d/49-sansserif.conf') as f:
                return '>sans-serif<' in f.read()
        except IOError: # File does not exist
            return False
    def cure(self):
        with TempOwn('/etc/fonts/conf.d/49-sansserif.conf') as o:
            with open('/etc/fonts/conf.d/49-sansserif.conf') as f:
                content = f.read()
            content = content.replace('>sans-serif<', '>sans serif<')
            with open('/etc/fonts/conf.d/49-sansserif.conf', 'w') as f:
                f.write(content)

class Add_user_to_vboxusers_group(C):
    __doc__ = _('Add yourself to "vboxusers" group. Otherwise, USB devices cannot be used in VirtualBox.')
    detail = _('Command:') + ' gpasswd -a $USER vboxusers'
    type = C.MUST_FIX
    def exists(self):
        username = os.environ['USER']
        with open('/etc/group') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('vboxusers:'):
                return not username in line
    def cure(self):
        command = os.path.expandvars('gpasswd -a $USER vboxusers')
        run_as_root(command)

class Fix_error_in_fontconfig_properties(C):
    __doc__ = _('Fix errors in Java font configuration. Otherwise, some unicode characters cannot be displayed.')
    detail = _('Change wqy-zenhei.ttf to wqy-zenhei.ttc. Change uming.ttf to uming.ttc.')
    type = C.MUST_FIX
    file = '/etc/java-6-openjdk/fontconfig.properties'
    def exists(self):
        try:
            with open(self.file) as f:
                content = f.read()
            return '/wqy-zenhei.ttf' in content or '/uming.ttf' in content
        except IOError:
            return False
    def cure(self):
        with TempOwn(self.file) as o:
            with open(self.file) as f:
                content = f.read()
            content = content.replace('/wqy-zenhei.ttf', '/wqy-zenhei.ttc')
            content = content.replace('/uming.ttf', '/uming.ttc')
            with open(self.file, 'w') as f:
                f.write(content)

class Fix_error_in_netbeans_shortcut(C):
    __doc__ = _('Fix errors in Netbeans shortcut. Otherwise, some unicode characters cannot be displayed.')
    detail = _("""Add "export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on'" """)
    type = C.MUST_FIX
    file = '/usr/share/applications/netbeans.desktop'
    def exists(self):
        try:
            with open(self.file) as f:
                content = f.read()
            return '\nExec=/usr/bin/netbeans\n' in content
        except IOError:
            return False
    def cure(self):
        with TempOwn(self.file) as o:
            with open(self.file) as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('Exec='):
                    lines[i] = """Exec=sh -c "_JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on' /usr/bin/netbeans" \n"""
            with open(self.file, 'w') as f:
                f.writelines(lines)
            
