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

class WINE(N):
    __doc__ = _('WINE')
    detail = _('This is an indispensable application for running Windows applications on Linux.')
    license = LGPL + ' http://wiki.winehq.org/Licensing'
    category = 'vm'
    if FEDORA:
        pkgs = 'wine'
    if UBUNTU or MINT:
        def __init__(self):
            if APT.exist('wine1.2') and APT.exist('wine1.2-gecko'):
                self.pkgs = 'wine1.2 wine1.2-gecko'
            else:
                self.pkgs = 'wine wine-gecko'
            N.__init__(self)

class Enhance_Decompression_Capability(N) :
    __doc__ = _('Compression/decompression support for "*.7z" and "*.cab" files')
    if FEDORA:
        pkgs = "p7zip cabextract"
    if UBUNTU or MINT:
        pkgs = "p7zip p7zip-rar p7zip-full cabextract unace"

class Evince_Read_Chinese_PDF(N) :
    __doc__ = _('Make Evince be able to reveal Chinese, Japanese, Korean pdf')
    category='office'
    if FEDORA:
        pkgs = 'poppler-data'
    if UBUNTU or MINT:
        pkgs = 'poppler-data'

class CHMSee_Read_CHM_Documents(N) :
    __doc__ = _('ChmSee: A CHM file viewer')
    category = 'office'
    license = GPL + ' http://code.google.com/p/chmsee/'
    if FEDORA:
        pkgs = 'chmsee'
    if UBUNTU or MINT:
        pkgs = 'chmsee'

class Workrave_And_Auto_Start_It(N) :
    __doc__ = 'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.')
    license = GPL + ' http://sourceforge.net/projects/workrave/'
    if FEDORA:
        pkgs = 'workrave'
    if UBUNTU or MINT:
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
        N.install(self)
        self.__workraveautostart()
    def installed(self):
        import os
        if not os.path.exists(self.file): return False
        return N.installed(self)
    def remove(self):
        N.remove(self)
        import os
        if os.path.exists(self.file):
            os.remove(self.file)

class VIM_and_VIMRC(N) :
    __doc__ = _('Make VIM more suitable for programming')
    detail = _('Install VIM and make it more suitable for programming. '
       'The installation process is as follows. '
       '"yum install vim-enhanced" command is executed. '
       'Then these lines are appended into "$HOME/.vimrc" file: \n'
       '    syntax on\n    set autoindent\n    set number\n    set mouse=a')
    license = GPL
    category = 'dev'
    if FEDORA:
        pkgs = 'vim-enhanced'
    if UBUNTU or MINT:
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
        N.install(self)
        self.__vimrc_install()
    def installed(self):
        return N.installed(self)
    def remove(self):
        N.remove(self)
        file_remove ( self.vimrc, *self.lines )

class Multimedia_Codecs (N) :
    __doc__ = _('Multi-media codec')
    category = 'media'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = ( 'gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad ' +
                 'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse' )

class Stardict_without_Dictionaries(N):
    __doc__ = _('Stardict')
    category = 'office'
    license = GPL
    if FEDORA:
        detail = _('You can install these dictionaries by yum.\n'
                   'stardict-dic-cs_CZ: Czech dictionaries\n'
                   'stardict-dic-en: English dictionaries\n'
                   'stardict-dic-hi: Hindi dictionary\n'
                   'stardict-dic-ja: Japanese dictionaries\n'
                   'stardict-dic-ru: Russian dictionaries\n'
                   'stardict-dic-zh_CN: Simplified Chinese dictionaries\n'
                   'stardict-dic-zh_TW: Traditional Chinese dictionaries')
        pkgs = 'stardict'
    if UBUNTU or MINT:
        pkgs = 'stardict'

class Liferea(N):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.')
    license = GPL
    category = 'internet'
    if FEDORA:
        pkgs = 'liferea'
    if UBUNTU or MINT:
        pkgs = 'liferea'

class FireWall(N):
    __doc__ = _('Firestarter: Configure Linux firewall')
    detail = _('Linux system comes up with a firewall "iptables". '
       'Firestarter is the graphical frontend of "iptables".')
    license = GPL
    category = 'internet'
    if UBUNTU or MINT:
        pkgs = 'firestarter'

class MACChanger(N):
    __doc__ = _('MACChanger: change MAC address')
    detail = _('MACChanger is a utility for viewing/manipulating the MAC address of network interfaces.')
    license = GPL
    category = 'hardware'
    if UBUNTU or MINT:
        pkgs = 'macchanger'

class Bluetooth(N):
    __doc__ = _('Bluetooth support')
    license = GPL
    category = 'hardware'
    if UBUNTU or MINT:
        pkgs = 'bluetooth bluez-alsa bluez-cups bluez-utils python-bluez gnome-bluetooth gnome-phone-manager'

class CommonUsedProgrammingPackages(N):
    __doc__ = _('Useful applications for programming')
    detail = _('The tools are:\n'
       '<i>'
       'gcc: GNU C compiler.\n'
       'gcc-c++: GNU C++ compiler.\n'
       'ctags: source code parser used in vi and emacs, which allow moving to the definition of a symbol.\n'
       'gmp-devel: GNU multiprecision arithmetic library.\n'
       'ncurses-devel: a library controlling writing to the console screen.\n'
       'qt3-devel: Trolltech Qt library, version 3.\n'
       'subversion: a version control system.\n'
       'git: a distributed version control system.'
       '</i>')
    category = 'dev'
    if FEDORA:
        pkgs = ('gcc gcc-c++ ctags gmp-devel ncurses-devel '
            'qt3-devel subversion git')

class QtiPlot(N) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.')
    category = 'math'
    license = GPL
    if FEDORA:
        pkgs = 'qtiplot'

class QCad(N):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    license = GPL
    category = 'em'
    if FEDORA:
        pkgs = 'qcad'

class Alacarte(N):
    __doc__ = ("Alacarte: menu editor")
    license = LGPL
    if FEDORA:
        pkgs = 'alacarte'
    
class Octave(N):
    __doc__ = _(u'Octave: A Matlab® compatible numerical computation appliation')
    license = GPL + ' http://www.gnu.org/software/octave/license.html'
    category = 'math'
    if FEDORA:
        pkgs = 'qtoctave'

class TuxPaint(N):
    __doc__ = _('Tux Paint: A drawing program for young children three years and up')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'tuxpaint'

class ChildsPlay(N):
    __doc__ = _('ChildsPlay: A suite of educational games for children')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'childsplay'
        
class GCompris(N):
    __doc__ = _('GCompris: Educational games for children aged 2 to 10')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'gcompris'

class QT_Creator(N):
    'Qt Creator'
    detail = _('This is an IDE for Qt.')
    category = 'dev'
    license = GPL
    if FEDORA:
        pkgs = 'qt-creator'

class Kadu(N):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.\n'
               'Command : yum install kadu')
    category = 'internet'
    license = GPL
    if FEDORA:
        pkgs = 'kadu'
    def visible(self):
        return Config.is_Poland_locale()

class Parcellite(N):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = GPL
    if FEDORA:
        pkgs = 'parcellite'

class Gnash(N):
    __doc__ = _('Flash plugin for web browser')
    category = 'media'
    license = GPL
    if FEDORA:
        pkgs = 'gnash gnash-plugin'
    if UBUNTU and MINT:
        pkgs = 'gnash mozilla-plugin-gnash'
    
class Nautilus_Actions(N):
    __doc__ = _('"Actions configuration" entry')
    detail = _('It allows the configuration of programs to be launched on files selected.\n'
               '<span color="red">This entry is not in context menu. It is in "System"->"Preferences" menu.</span>')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-actions'
        
class Nautilus_Image_Converter(N):
    __doc__ = _('"Resize/Rotate images" entries')
    detail = _('Resize or rotate selected images.')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-image-converter'
        
class Nautilus_Open_Terminal(N):
    __doc__ = _('"Open in terminal" entry')
    detail = _('Open a terminal in current folder.')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-open-terminal'
        
class Nautilus_Search_Tool(N):
    __doc__ = _('"Search files" entries')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-search-tool'

class ImageMagick(N):
    __doc__ = _('ImageMagick: Edit images')
    detail = _('You can start it by /usr/bin/display')
    category = 'media'
    if FEDORA:
        pkgs = 'ImageMagick'

class PiTiVi(N):
    __doc__ = _('PiTiVi: Movie editor')
    license = LGPL + ' http://www.pitivi.org/'
    category = 'media'
    if FEDORA:
        pkgs = 'pitivi'

class Audacity(N):
    __doc__ = _('Audacity: Music editor')
    license = LGPL + ' http://audacity.sourceforge.net/'
    category = 'media'
    if FEDORA:
        pkgs = 'audacity-freeworld'

class WorldofPadman(N):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.\n'
               'Download from ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/')
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'game'
    if FEDORA:
        pkgs = 'worldofpadman'

class HardwareLister(N):
    __doc__ = _('lshw: List hardware information')
    detail = _('A small application which displays detailed hardware information')
    license = GPL
    category = 'hardware'
    if FEDORA:
        pkgs = 'lshw lshw-gui'

class Typespeed(N) :
    'Typespeed'
    detail= _('Typespeed is a typing practise. It only runs in terminal.')
    category = 'game'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = "typespeed"

class Full_Language_Pack(N):
    __doc__ = _('Full language support and input method')
    detail = _('Because of live CD capacity limitation, this Linux distribution does not have full language support.\n')
    category = 'language'
    if UBUNTU or MINT:
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
            
            N.__init__(self)

class Build_Essential(N):
    'Build-essential'
    detail = _('By installing build-essential, you will get g++, make, gdb and libc.')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'build-essential'

class POSIX_ManPages(N):
    __doc__ = _('POSIX library manual pages')
    detail = _('Install manual pages about Linux system calls, library calls, and POSIX libraries.')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'manpages-dev manpages-posix manpages-posix-dev'

class Ctags_Cscope(N):
    __doc__ = _('Ctags and Cscope: Popular source code parsers')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'exuberant-ctags cscope'

class GMP(N):
    __doc__ = _('GNU multiprecision arithmetic library')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'libgmp3-dev'

class Ncurses_and_qt3mt(N):
    __doc__ = _('Ncurses5 and QT3')
    detail = _('libncurses5 is a library controlling writing to the console screen.\n'
               'libqt3-mt is Trolltech Qt library, version 3.') 
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'libncurses5-dev libqt3-mt-dev'
        
class Svn_Git_bzr(N):
    __doc__ = _('Subversion, Git and Bzr: Popular version control systems')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'subversion git-core bzr'
        
class AutoTools(N):
    __doc__ = _('Autoconf and Automake: Generate configure scripts and Makefiles')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'autoconf automake'
        
class FreeGLut3(N):
    __doc__ = _('OpenGL library')  
    detail = _('This is a library for writing OpenGL programs.')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'freeglut3-dev'
        
class Boost(N):
    __doc__ = _('Boost library')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'libboost-dev'

class SDL(N):
    __doc__ = _('SDL library')
    detail = _('This is a library for writing SDL programs.\n'
               'SDL is a cross-platform multimedia library designed to provide low level access to audio'
               ' keyboard, mouse, joystick, 3D hardware via OpenGL, and 2D video framebuffer.')
    category = 'dev'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = 'libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev'
