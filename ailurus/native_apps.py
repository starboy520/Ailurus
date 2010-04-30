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
        
class Enhance_Decompression_Capability(N) :
    __doc__ = _('Compression/decompression support for "*.7z" and "*.cab" files')
    if FEDORA:
        pkgs = "p7zip cabextract"

class Evince_Read_Chinese_PDF(N) :
    __doc__ = _('Make Evince be able to reveal Chinese, Japanese, Korean pdf')
    category='office'
    if FEDORA:
        pkgs = 'poppler-data'

class CHMSee_Read_CHM_Documents(N) :
    __doc__ = _('ChmSee: A CHM file viewer')
    category = 'office'
    license = GPL + ' http://code.google.com/p/chmsee/'
    if FEDORA:
        pkgs = 'chmsee'

class Workrave_And_Auto_Start_It(N) :
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

class CUPS (N):
    __doc__ = _('Enable "Print to pdf" capability.')
    category = 'office'
    if FEDORA:
        pkgs = 'cups-pdf'

class Stardict_without_Dictionaries(N):
    __doc__ = _('Stardict')
    category = 'office'
    detail = _('You can install these dictionaries by yum.\n'
               'stardict-dic-cs_CZ: Czech dictionaries\n'
               'stardict-dic-en: English dictionaries\n'
               'stardict-dic-hi: Hindi dictionary\n'
               'stardict-dic-ja: Japanese dictionaries\n'
               'stardict-dic-ru: Russian dictionaries\n'
               'stardict-dic-zh_CN: Simplified Chinese dictionaries\n'
               'stardict-dic-zh_TW: Traditional Chinese dictionaries')
    license = GPL
    if FEDORA:
        pkgs = 'stardict'

class Liferea(N):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.')
    license = GPL
    category = 'internet'
    if FEDORA:
        pkgs = 'liferea'

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
    def support(self):
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
