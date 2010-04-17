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

class Full_Language_Pack(_apt_install):
    __doc__ = _('Full language support and input method')
    detail = _('Because of live CD capacity limitation, the Ubuntu system does not have full language support.\n')
    logo = 'language.png'
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

#class Eliminate_SCIM_Crash_Bug(_apt_install):
#    __doc__ = _('Eliminate bug: SCIM suddenly crashes without reason')
#    size = 172 * 1000
#    logo = 'scim.png'
#    pkgs='scim-bridge-client-qt'
#    def support(self):
#        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty'] and APT.installed('scim')

class Decompression_Capability(_apt_install) :
    __doc__ = _('Decompression software: 7z, rar, cab, ace')
    detail = _('Command: sudo apt-get install p7zip p7zip-rar p7zip-full cabextract unace')
    logo = 'extract.png'
    license = 'GPL'
    pkgs = "p7zip p7zip-rar p7zip-full cabextract unace"

class Typespeed(_apt_install) :
    'Typespeed'
    detail= _('Typespeed is a typing practise. It only runs in terminal.')
    size = 356 * 1000
    category = 'game'
    logo = 'typespeed.png'
    license = 'GNU Lesser General Public License (LGPL)'
    pkgs = "typespeed"

class Evince_Read_Chinese_PDF(_apt_install) :
    __doc__ = _('Make Evince be able to reveal Chinese, Japanese, Korean pdf')
    detail = _('Command: sudo apt-get install poppler-data')
    category='office'
    Chinese = True
    size = 12276 * 1000
    logo = 'evince.png'
    pkgs = 'poppler-data'

class CHMSee_Read_CHM_Documents(_apt_install) :
    __doc__ = _('ChmSee: A CHM file viewer')
    detail = _('Command: sudo apt-get install chmsee')
    license = ('GNU General Public License (GPL), '
               'see http://code.google.com/p/chmsee/')
    category = 'office'
    size = 590 * 1000
    logo = 'chmsee.png'
    pkgs = 'chmsee'

class Workrave_And_Auto_Start_It(_apt_install) :
    __doc__ = 'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.\n'
       'Command: sudo apt-get install workrave')
    license = ('GNU General Public License (GPL)'
                'see http://sourceforge.net/projects/workrave/')
    size = 1012 * 1000
    logo = 'workrave.png'
    pkgs = 'workrave'
    def __init__(self):
        import os
        self.path = os.path.expanduser('~/.config/autostart/')
        self.file = self.path + 'workrave.desktop'
    def __workraveautostart(self):
        if not os.path.exists(self.path):
            run('mkdir -p '+self.path)
        with open(self.file, 'w') as f:
            f.write(
'''[Desktop Entry]
Name=Workrave
Exec=workrave
Encoding=UTF-8
Version=1.0
Type=Application
X-GNOME-Autostart-enabled=true
'''
            )
    def install(self):
        _apt_install.install(self)
        self.__workraveautostart()
    def installed(self):
        import os
        if not os.path.exists(self.file): return False
        return _apt_install.installed(self)
    def remove(self):
        _apt_install.remove(self)
        import os
        if os.path.exists(self.file):
            os.remove(self.file)

class VIM_and_VIMRC(_apt_install) :
    __doc__ = _('Make VIM more suitable for programming')
    detail = _('Install VIM and make it more suitable for programming. '
       'The installation process is as follows. '
       '"sudo apt-get install vim" command is executed. '
       'Then these lines are appended into "$HOME/.vimrc" file: \n'
       '    syntax on\n    set autoindent\n    set number\n    set mouse=a')
    category = 'dev'
    license = 'GNU General Public License (GPL)'
    size = 1892 * 1000
    logo = 'vim.png'
    pkgs = 'vim'
    def __vimrc_installed(self):
        return file_contain ( self.vimrc, *self.lines )
    def __vimrc_install(self):
        file_append ( self.vimrc, *self.lines )
    def __init__(self):
        import os
        self.vimrc = os.path.expanduser("~/.vimrc")
        self.lines = [ 'syntax on', 'set autoindent', 'set number', 'set mouse=a' ]
    def install(self):
        _apt_install.install(self)
        self.__vimrc_install()
    def installed(self):
        return _apt_install.installed(self)
    def remove(self):
        _apt_install.remove(self)
        file_remove ( self.vimrc, *self.lines )

class ColorfulBashPromptSymbols :
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = _('Change Bash prompt symbols from '
       '"username@hostname:~$ " to '
       '"<span color="#3dba34">username@hostname</span>:'
       '<span color="#729fcf">~</span>$ ".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '")
    logo = 'terminal.png'
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
        
class Multimedia_Codecs (_apt_install) :
    __doc__ = _('Multi-media codec')
    detail = _(
       'Command: sudo apt-get install gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad '
       'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse')
    category = 'media'
    license = 'GNU Lesser General Public License'
    size = 6868 * 1000
    logo = 'codec.png'
    pkgs = ( 'gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad ' +
             'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse' )

class Eliminate_CUPS_Cannot_Print_Bug(_apt_install):
    __doc__ = _('Enable "Print to pdf" capability and eliminate "Cannot print" bug')
    detail = _('The installation process is as follows. Firstly, the command "sudo apt-get install cups-pdf" is launched. '
       'Then a bug in "/etc/apparmor.d/usr.sbin.cupsd" file is eliminated.')
    __line = '/usr/lib/cups/backend/cups-pdf flags=(complain) {\n'
    __file = '/etc/apparmor.d/usr.sbin.cupsd'
    size = 256 * 1000
    category = 'office'
    license = 'GNU Lesser General Public License'
    logo = 'cups.png'
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
        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty']

class CUPS(_apt_install):
    __doc__ = _('Enable "Print to pdf" capability')
    detail = _('Command: sudo apt-get install cups-pdf')
    license = 'GNU Lesser General Public License'
    category = 'office'
    logo = 'cups.png'
    pkgs = 'cups-pdf'
    def support(self):
        return Config.get_Ubuntu_version() not in ['hardy', 'intrepid', 'jaunty']
        
class Flash_Player(_apt_install):
    __doc__ = _(u'GNU Flash plugin for web browser')
    detail = _('Command: sudo apt-get install gnash mozilla-plugin-gnash')
    category = 'media'
    license = 'GPL'
    logo = 'flash.png'
    pkgs = 'gnash mozilla-plugin-gnash'
    
#class Flash_Player_Font_Bug:
#    __doc__ = _('Fix font bug in Flash plugin')
#    detail = _('Fix bug: characters are displayed as blank square in Flash.\n'
#       'The trick behind is to modify "/etc/fonts/conf.d/49-sansserif.conf" file.')
#    category = 'media'
#    logo = 'flash.png'
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

class Stardict(_apt_install):
    __doc__ = _('Stardict')
    category = 'office'
    detail = 'Command: sudo apt-get install stardict'
    license = 'GNU General Public License (GPL)'
    logo = 'stardict.png'
    pkgs = 'stardict'
        
class Liferea(_apt_install):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.\n'
       'Command: sudo apt-get install liferea')
    category = 'internet'
    license = 'GNU General Public License (GPL)'
    size = 3792 * 1000
    logo = 'liferea.png'
    pkgs = 'liferea'

class FireWall(_apt_install):
    __doc__ = _('Firestarter: Configure Linux firewall')
    detail = _('Linux system comes up with a firewall "iptables". '
       'Firestarter is the graphical frontend of "iptables".\n'
       'Command: sudo apt-get install firestarter')
    license = 'GNU General Public License (GPL)'
    category = 'internet'
    size = 1980 * 1000
    logo = 'firestarter.png'
    pkgs = 'firestarter'

class MACChanger(_apt_install):
    __doc__ = _('MACChanger: change MAC address')
    detail = _('MACChanger is a utility for viewing/manipulating the MAC address of network interfaces.\n'
               'Command: sudo apt-get install macchanger')
    license = 'GNU General Public License (GPL)'
    category = 'hardware'
    pkgs = 'macchanger'

class Bluetooth(_apt_install):
    __doc__ = _('Bluetooth support')
    detail = _('Command: sudo apt-get install bluetooth bluez-alsa bluez-cups bluez-utils python-bluez gnome-bluetooth gnome-phone-manager')
    license = 'GNU General Public License (GPL)'
    logo = 'bluetooth.png'
    category = 'hardware'
    pkgs = 'bluetooth bluez-alsa bluez-cups bluez-utils python-bluez gnome-bluetooth gnome-phone-manager'
