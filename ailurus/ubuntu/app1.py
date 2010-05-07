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

class Full_Language_Pack(_apt_install):
    __doc__ = _('Full language support and input method')
    detail = _('Because of live CD capacity limitation, the Ubuntu system does not have full language support.\n')
    category = 'language'
    def __init__(self):
        import locale
        lang = locale.getdefaultlocale()
        try:
            lang = lang[0].split('_')[0]
        except AttributeError: # lang == null
            lang = 'en'

        List = [
                'language-pack-' + lang,
                'language-support-fonts-' + lang,
                'language-support-input-' + lang,
                'language-support-translations-' + lang,
                'language-support-' + lang,
                'language-support-writing-' + lang,
                ]
        try:
            get_output('pgrep -u $USER gnome-panel')
            List.append('language-pack-gnome-' + lang)
        except: pass

        pkgs = []
        for p in List:
            if APT.exist(p): pkgs.append(p)

        self.pkgs = ' '.join(pkgs)

        if not getattr(self.__class__, 'appended', False) and hasattr(self, 'pkgs'):
            self.__class__.appended = True
            self.__class__.detail += _('Command: ')+'sudo apt-get install '+self.pkgs

class ColorfulBashPromptSymbols(I):
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = _('Change Bash prompt symbols from '
       '"username@hostname:~$ " to '
       '"<span color="#3dba34">username@hostname</span>:'
       '<span color="#729fcf">~</span>$ ".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '")
    def __init__(self):
        self.line = r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '"
        import os
        self.bashrc = os.path.expandvars('$HOME/.bashrc')
    def install(self):
        file_append ( self.bashrc, self.line )
        notify( _('The color of bash prompt symbols is changed.'), _('It will take effect at the next time you log in.') )
    def installed(self):
        return file_contain ( self.bashrc, self.line )
    def remove(self):
        file_remove ( self.bashrc, self.line )
        
class Eliminate_CUPS_Cannot_Print_Bug(_apt_install):
    __doc__ = _('Enable "Print to pdf" capability and eliminate "Cannot print" bug')
    detail = _('The installation process is as follows. Firstly, the command "sudo apt-get install cups-pdf" is launched. '
       'Then a bug in "/etc/apparmor.d/usr.sbin.cupsd" file is eliminated.')
    __line = '/usr/lib/cups/backend/cups-pdf flags=(complain) {\n'
    __file = '/etc/apparmor.d/usr.sbin.cupsd'
    category = 'office'
    license = LGPL
    pkgs = 'cups-pdf'
    def install(self):
        _apt_install.install(self)
        run_as_root("chmod 4755 /usr/lib/cups/backend/cups-pdf") #rwsr-xr-x
        with TempOwn( self.__file ) as o:
            with open( self.__file , "r") as f:
                content = f.readlines()
                for i in range(0, len(content)):
                    if content[i].find('/usr/lib/cups/backend/cups-pdf')==0:
                        content[i]=self.__line
                        break
            with open( self.__file , "w") as f:
                for c in content:
                    f.write(c)
    def installed(self):
        return _apt_install.installed(self) and file_contain(self.__file, self.__line)
    def support(self):
        return VERSION in ['hardy', 'intrepid', 'jaunty']

#class Flash_Player_Font_Bug:
#    __doc__ = _('Fix font bug in Flash plugin')
#    detail = _('Fix bug: characters are displayed as blank square in Flash.\n'
#       'The trick behind is to modify "/etc/fonts/conf.d/49-sansserif.conf" file.')
#    category = 'media'
#    __file = '/etc/fonts/conf.d/49-sansserif.conf' 
#    def installed(self):
#        import os
#        return not os.path.exists(self.__file)
#    def install(self):
#        with Chdir('/etc/fonts/conf.d') as o:
#            import os
#            if os.path.exists('49-sansserif.conf'):
#                run_as_root('mv 49-sansserif.conf 49-sansserif.back')
#    def remove(self):
#        with Chdir('/etc/fonts/conf.d') as o:
#            import os
#            if os.path.exists('49-sansserif.back'):
#                run_as_root('mv 49-sansserif.back 49-sansserif.conf')
#    def get_reason(self, f):
#        import os
#        if os.path.exists(self.__file):
#            print >>f, _('The file "%s" exists.')%self.__file

class WorldofPadman(I):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.\n'
               'Download from ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/')
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'game'
    def install(self):
        file1 = R('ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/worldofpadman.run').download()
        run_as_root('bash ' + file1)
        file2 = R('ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/wop_patch_1_2.run').download()
        run_as_root('bash ' + file2)
        
    def installed(self):
        import os
        return os.path.exists('/usr/local/games/WoP')
        
    def remove(self):
        run_as_root('rm /usr/local/games/WoP -rf')
        run_as_root('rm /usr/local/bin/wop')
