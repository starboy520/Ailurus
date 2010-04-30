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

class CreateDesktopFolder(I):
    __doc__ = _('Create a directory "Desktop" in your home folder')
    detail = _('Create a directory "Desktop" which is linked to the desktop. After that, you can chdir to the desktop folder by command "cd ~/Desktop".')
    def __init__(self):
        import os
        self.desktop = os.path.expanduser('~/Desktop')
    def install(self):
        import os
        if not os.path.exists(self.desktop):
            # read file
            with open( os.path.expanduser('~/.config/user-dirs.dirs') ) as f:
                contents = f.readlines()
            # get name
            name = None
            for line in contents:
                if line.strip()[0] == '#': continue
                if 'XDG_DESKTOP_DIR' in line:
                    name = line.strip().split('=')[1]
                    if name[0] == '"' and name[-1] == '"': name = name[1:-1]
                    name = os.path.expandvars(name)
            # create link
            if name and os.path.exists(name):
                run('ln -s %s %s'%(name,self.desktop))
    def installed(self):
        import os 
        return os.path.exists(self.desktop)
    def remove(self):
        import os
        if os.path.islink(self.desktop):
            run('rm -f '+self.desktop)

class Speed_Up_Firefox(I):
    __doc__ = _('Speed up Firefox')
    detail = _('Firefox is faster when Pango rendering is disabled. '
        'The trick is to launch Firefox by the command: "export MOZ_DISABLE_PANGO=1; firefox". '
        'Ailurus will create a new icon "Firefox without Pango (faster)" in the menu "Applications"-->"Internet".')
    def install(self):
        paths = [
                 '/usr/share/applications/firefox-3.5.desktop',
                 '/usr/share/applications/firefox.desktop', 
                 '/usr/share/applications/mozilla-firefox.desktop',
                 '/usr/share/applications/abrowser.desktop',
                 ]
        for path in paths:
            import os
            if os.path.exists(path): break
        else:
            raise Exception('Firefox shortcut is not found.')
            
        with open(path) as f:
            content = f.readlines()
        for i, line in enumerate(content):
            if line.startswith('Exec='):
                firefox_launcher = line.split('=')[1].strip()
                new = 'Exec=sh -c "export MOZ_DISABLE_PANGO=1; %s"\n'%firefox_launcher
                content[i] = new
            if line.startswith('Name='):
                content[i] = 'Name=%s\n'%_('Firefox without Pango (faster)')
        dir = '/usr/local/share/applications/'
        if not os.path.exists(dir): run_as_root('mkdir ' + dir)
        with TempOwn(dir + 'firefox.nopango.desktop') as o:
            with open(dir + 'firefox.nopango.desktop', 'w') as f:
                f.writelines(content)

    def installed(self):
        import os 
        return ( os.path.exists('/usr/local/share/applications/firefox.nopango.desktop') or
                 os.path.exists('/usr/share/applications/firefox.nopango.desktop') )
    def remove(self):
        run_as_root('rm -f /usr/local/share/applications/firefox.nopango.desktop')
        run_as_root('rm -f /usr/share/applications/firefox.nopango.desktop')

class QueryBeforeRmALotFiles(I) :
    __doc__ = _('Query you before delete more than three files')
    detail = _('If you try to delete more than three files by "rm *", '
       'BASH will ask you a question "remove all argument?" to make sure if you really want to delete files. '
       'This is useful if you mistype "rm subdir/*" as "rm subdir/ *".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       'alias rm="rm -I"')
    def __init__(self):
        self.line = r"alias rm='rm -I'"
        import os
        self.bashrc = os.path.expandvars('$HOME/.bashrc')
    def install(self):
        file_append ( self.bashrc, self.line )
    def installed(self):
        return file_contain ( self.bashrc, self.line )
    def remove(self):
        file_remove ( self.bashrc, self.line )

class Enhance_Decompression_Capability(_rpm_install) :
    __doc__ = _('Compression/decompression support for "*.7z" and "*.cab" files')
    if FEDORA:
        pkgs = "p7zip cabextract"

class Workrave_And_Auto_Start_It(_rpm_install) :
    __doc__ = 'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.')
    license = GPL + ' http://sourceforge.net/projects/workrave/'
    if FEDORA:
        pkgs = 'workrave'
        def __init__(self):
            import os
            self.path = os.path.expanduser('~/.config/autostart/')
            self.file = self.path + 'workrave.desktop'
        def __workraveautostart(self):
            if not os.path.exists(self.path):
                run('mkdir -p '+self.path)
            with open(self.file, 'w') as f:
                f.write('[Desktop Entry]\n'
                        'Name=Workrave\n'
                        'Exec=workrave\n'
                        'Encoding=UTF-8\n'
                        'Version=1.0\n'
                        'Type=Application\n'
                        'X-GNOME-Autostart-enabled=true\n')
        def install(self):
            _rpm_install.install(self)
            self.__workraveautostart()
        def installed(self):
            import os
            if not os.path.exists(self.file): return False
            return _rpm_install.installed(self)
        def remove(self):
            _rpm_install.remove(self)
            import os
            if os.path.exists(self.file):
                os.remove(self.file)

if FEDORA:
    class ColorfulBashPromptSymbols(I):
        __doc__ = _('Use colorful Bash prompt symbols')
        detail = _('Change Bash prompt symbols from '
           '"[username@hostname ~]$ " to '
           '"<span color="#3dba34">username@hostname</span> '
           '<span color="#729fcf">~</span>$ ".\n'
           'The trick behind is to add this line into "$HOME/.bashrc".\n'
           r"PS1='\[\033[01;32m\]\u@\h\[\033[00m\] \[\033[01;34m\]\W\[\033[00m\]\\$ '")
        def __init__(self):
            import os
            self.__class__.detail = os.path.expandvars( self.__class__.detail )
            self.line = r"PS1='\[\033[01;32m\]\u@\h\[\033[00m\] \[\033[01;34m\]\W\[\033[00m\]\\$ '"
            self.bashrc = os.path.expandvars('$HOME/.bashrc')
        def install(self):
            file_append ( self.bashrc, self.line )
            notify( _('The color of bash prompt symbols is changed.'), _('It will take effect at the next time you log in.') )
        def installed(self):
            return file_contain ( self.bashrc, self.line )
        def remove(self):
            file_remove ( self.bashrc, self.line )

