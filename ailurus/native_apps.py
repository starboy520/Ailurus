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

class Alacarte(N):
    __doc__ = ("Alacarte: menu editor")
    license = LGPL
    if FEDORA:
        pkgs = 'alacarte'
    
class Audacity(N):
    __doc__ = _('Audacity: Music editor')
    license = LGPL + ' http://audacity.sourceforge.net/'
    category = 'media'
    if FEDORA:
        pkgs = 'audacity-freeworld'

class AutoApt(N):
    'Auto-apt'
    detail = _('"auto-apt run ./configure" can help you install the packages which are not installed.')
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'auto-apt'

class AutoTools(N):
    __doc__ = _('Autoconf and Automake: Generate configure scripts and Makefiles')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'autoconf automake'
        
class Bluefish(N):
    __doc__ = _('Bluefish: Edit HTML web-pages')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'bluefish'

class Bluetooth(N):
    __doc__ = _('Bluetooth support')
    license = GPL
    category = 'hardware'
    if UBUNTU or MINT:
        pkgs = 'bluetooth bluez-alsa bluez-cups bluez-utils python-bluez gnome-bluetooth gnome-phone-manager'

class Boost(N):
    __doc__ = _('Boost library')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'libboost-dev'

class Build_Essential(N):
    'Build-essential'
    detail = _('By installing build-essential, you will get g++, make, gdb and libc.')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'build-essential'

class CHMSee_Read_CHM_Documents(N) :
    __doc__ = _('ChmSee: A CHM file viewer')
    category = 'office'
    license = GPL + ' http://code.google.com/p/chmsee/'
    if FEDORA:
        pkgs = 'chmsee'
    if UBUNTU or MINT:
        pkgs = 'chmsee'

class CheckInstall(N):
    'CheckInstall'
    detail = _('Checkinstall help you build deb package.')
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'checkinstall'
        
class ChildsPlay(N):
    __doc__ = _('ChildsPlay: A suite of educational games for children')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'childsplay'
        
class ChildsPlay(N):
    __doc__ = _('ChildsPlay: A suite of educational games for children')
    category = 'education'
    license = GPL
    if UBUNTU or MINT:
        def __init__(self):
            pkgs = APT.get_existing_pkgs_set()
            voices = [ e for e in pkgs if e.startswith('childsplay-alphabet-sounds-') ]
            lang = Config.get_locale().split('_')[0]
            voice = 'childsplay-alphabet-sounds-'+lang
            if not voice in voices: voice = ''
            else: voice = ' ' + voice
            self.pkgs = 'childsplay' + voice
            # There is no 'childsplay-plugins-lfc' package in Karmic :)
            # 'childsplay-plugins-lfc' is letterFlashscard game.
            if APT.exist('childsplay-plugins-lfc'):
                self.pkgs += ' childsplay-plugins-lfc'
        
class CodeBlocks(N):
    __doc__ = _('Code::Blocks - C/C++ IDE')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'codeblocks'

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

class CompizSettingManager(N):
    __doc__ = _('Compiz settings manager')
    detail = _('Compiz Fusion is the unification of the Beryl project and the community around the Compiz Window Manager. '
       'Compiz settings manager is the configuration application for Compiz Fusion. '
       'It can configurate effects such as "Desktop cube" and "3D windows".')
    category = 'appearance'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'compizconfig-settings-manager'

class CompizSettingManagerSimple(N):
    __doc__ = _('Simple-ccsm: A simple Compiz settings manager')
    category = 'appearance'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'simple-ccsm'

class Ctags_Cscope(N):
    __doc__ = _('Ctags and Cscope: Popular source code parsers')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'exuberant-ctags cscope'

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

class Extcalc(N):
    __doc__ = _('Extcalc: A multifunctional graphic calculator')
    category = 'math'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'extcalc'
        
class Fcitx(N):
    'Fcitx'
    category = 'language'
    detail = _('This is a popular Chinese input method.\n'
               'It is from http://fcitx.googlecode.com/')
    Chinese = True
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'fcitx'

class FireWall(N):
    __doc__ = _('Firestarter: Configure Linux firewall')
    detail = _('Linux system comes up with a firewall "iptables". '
       'Firestarter is the graphical frontend of "iptables".')
    license = GPL
    category = 'internet'
    if UBUNTU or MINT:
        pkgs = 'firestarter'

class FreeGLut3(N):
    __doc__ = _('OpenGL library')  
    detail = _('This is a library for writing OpenGL programs.')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'freeglut3-dev'
        
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

class GCompris(N):
    __doc__ = _('GCompris: Educational games for children aged 2 to 10')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'gcompris'

class GCompris(N):
    __doc__ = _('GCompris: Educational games for children aged 2 to 10')
    category = 'education'
    license = GPL
    if UBUNTU or MINT:
        def __init__(self):
            pkgs = APT.get_existing_pkgs_set()
            voices = [ e for e in pkgs if e.startswith('gcompris-sound-') ]
            lang = Config.get_locale().split('_')[0]
            voice = 'gcompris-sound-'+lang
            if not voice in voices: voice = ''
            else: voice = ' ' + voice
            self.pkgs = 'gnucap gcompris' + voice
 
class GMP(N):
    __doc__ = _('GNU multiprecision arithmetic library')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'libgmp3-dev'

class Gnash(N):
    __doc__ = _('Flash plugin for web browser')
    category = 'media'
    license = GPL
    if FEDORA:
        pkgs = 'gnash gnash-plugin'
    if UBUNTU and MINT:
        pkgs = 'gnash mozilla-plugin-gnash'
    
class HardwareLister(N):
    __doc__ = _('lshw: List hardware information')
    detail = _('A small application which displays detailed hardware information')
    license = GPL
    category = 'hardware'
    if FEDORA:
        pkgs = 'lshw lshw-gui'

class HardwareLister(N):
    __doc__ = _('lshw: List hardware information')
    detail = _('A small application which displays detailed hardware information')
    license = GPL
    category = 'hardware'
    if UBUNTU or MINT:
        pkgs = 'lshw lshw-gtk'

class ImageMagick(N):
    __doc__ = _('ImageMagick: Edit images')
    detail = _('You can start it by /usr/bin/display')
    category = 'media'
    if FEDORA:
        pkgs = 'ImageMagick'

class ImageMagick(N):
    __doc__ = _('ImageMagick: Edit images')
    detail = _('You can start it by /usr/bin/display')
    category = 'media'
    if UBUNTU or MINT:
        pkgs = 'imagemagick'
        
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

class Kadu(N):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.')
    category = 'internet'
    if UBUNTU or MINT:
        pkgs = 'kadu'
        def visible(self):
            return Config.is_Poland_locale()

class Liferea(N):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.')
    license = GPL
    category = 'internet'
    if FEDORA:
        pkgs = 'liferea'
    if UBUNTU or MINT:
        pkgs = 'liferea'

class MACChanger(N):
    __doc__ = _('MACChanger: change MAC address')
    detail = _('MACChanger is a utility for viewing/manipulating the MAC address of network interfaces.')
    license = GPL
    category = 'hardware'
    if UBUNTU or MINT:
        pkgs = 'macchanger'

class MiniCom_Ckermit(N):
    __doc__ = _('Minicom and Kermit: Communication software for embedded MCU boards')
    license = GPL
    category = 'embedded'
    if UBUNTU or MINT:
        pkgs = 'minicom ckermit'

class Moonlight(N):
    __doc__ = _(u'Moonlight: an open source implementation of Microsoft® Silverlight')
    detail = _(u'Moonlight provides Windows® media codecs. '
       u'By this application, you can enjoy Windows® video/audio in webpages.')
    license = ('Moonlight 2.0 is licensed under LGPL and MIT X11 licenses. '
               'Moonlight 1.0 is licensed under LGPL. '
               'See http://www.mono-project.com/Moonlight')
    category = 'media'
    if UBUNTU or MINT:
        pkgs = 'moonlight-plugin-mozilla'

class Multimedia_Codecs (N) :
    __doc__ = _('Multi-media codec')
    category = 'media'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = ( 'gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad ' +
                 'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse' )

class Nautilus_Actions(N):
    __doc__ = _('"Actions configuration" entry')
    detail = _('It allows the configuration of programs to be launched on files selected.\n'
               '<span color="red">This entry is not in context menu. It is in "System"->"Preferences" menu.</span>')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-actions'
        
class Nautilus_Actions(N):
    __doc__ = _('"Actions configuration" entry')
    detail = _('It allows the configuration of programs to be launched on files selected.\n'
               '<span color="red">This entry is not in context menu. It is in "System"->"Preferences" menu.</span>')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-actions'
        
class Nautilus_Audio_Convert(N):
    __doc__ = _('"Convert audio files" entry')
    detail = _('Converts between WAV, OGG, MP3, MPC, FLAC, APE and AAC files.\n'
               'These packages will also be installed: \n'
               '<i>lame libid3-3.8.3-dev flac faac faad mppenc</i>')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-script-audio-convert lame libid3-3.8.3-dev flac faac faad mppenc'
        def install(self):
            N.install(self)
            run('nautilus-script-manager enable ConvertAudioFile')

class Nautilus_Filename_Repairer(N):
    __doc__ = _('"Repair filename" entry')
    detail = _('When any file with wrong encoding filename is right clicked,\n show a "Repair filename" menu item.')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-filename-repairer'

class Nautilus_Gksu(N):
    __doc__ = _('"Open as administrator" entry')
    detail = _('Launch selected files with administration privileges using the context menu.\nOpen selected folder with administration privileges.')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-gksu'

class Nautilus_Image_Converter(N):
    __doc__ = _('"Resize/Rotate images" entries')
    detail = _('Resize or rotate selected images.')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-image-converter'
        
class Nautilus_Image_Converter(N):
    __doc__ = _('"Resize/Rotate images" entries')
    detail = _('Resize or rotate selected images.')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-image-converter'
        
class Nautilus_Open_Terminal(N):
    __doc__ = _('"Open in terminal" entry')
    detail = _('Open a terminal in current folder.')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-open-terminal'
        
class Nautilus_Open_Terminal(N):
    __doc__ = _('"Open in terminal" entry')
    detail = _('Open a terminal in current folder.')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-open-terminal'
        
class Nautilus_Script_Collection_Svn(N):
    __doc__ = _('"Subversion commands" entries')
    detail = _('"Subversion commands" entries')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-script-collection-svn'
        def install(self):
            N.install(self)
            run('nautilus-script-manager enable Subversion')
        
class Nautilus_Search_Tool(N):
    __doc__ = _('"Search files" entries')
    license = GPL
    category = 'nautilus'
    if FEDORA:
        pkgs = 'nautilus-search-tool'

class Nautilus_Share(N):
    __doc__ = _('"Share folders" entry')
    detail = _('Share folders by Samba.')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-share'
        
class Nautilus_Wallpaper(N):
    __doc__ = _('"Set as wallpaper" entry')
    detail = _('"Set as wallpaper" entry')
    license = GPL
    category = 'nautilus'
    if UBUNTU or MINT:
        pkgs = 'nautilus-wallpaper'

class Ncurses_and_qt3mt(N):
    __doc__ = _('Ncurses5 and QT3')
    detail = _('libncurses5 is a library controlling writing to the console screen.\n'
               'libqt3-mt is Trolltech Qt library, version 3.') 
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'libncurses5-dev libqt3-mt-dev'
        
class Netbeans(N):
    __doc__ = 'Netbeans'
    detail = (
              _('It is an open source IDE which supports several languages (C, C++, Java, Ruby, etc.)'
               ' and frameworks (J2SE, J2ME, etc.). '
               'Official site: http://netbeans.org/downloads/ .') +
              _(' This application depends on Java.') )
    category = 'dev'
    license = DUAL_LICENSE(CDDL, GPL) + ' http://netbeans.org/about/legal/license.html'
    if UBUNTU or MINT:
        pkgs = 'netbeans'

class Octave(N):
    __doc__ = _(u'Octave: A Matlab® compatible numerical computation appliation')
    license = GPL + ' http://www.gnu.org/software/octave/license.html'
    category = 'math'
    if FEDORA:
        pkgs = 'qtoctave'

class Octave(N):
    __doc__ = _(u'Octave: A Matlab® compatible numerical computation appliation')
    license = GPL
    category = 'math'
    if UBUNTU or MINT:
        pkgs = 'qtoctave'

class POSIX_ManPages(N):
    __doc__ = _('POSIX library manual pages')
    detail = _('Install manual pages about Linux system calls, library calls, and POSIX libraries.')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'manpages-dev manpages-posix manpages-posix-dev'

class Parcellite(N):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = GPL
    if FEDORA:
        pkgs = 'parcellite'

class Parcellite(N):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'parcellite'

class PiTiVi(N):
    __doc__ = _('PiTiVi: Movie editor')
    license = LGPL + ' http://www.pitivi.org/'
    category = 'media'
    if FEDORA:
        pkgs = 'pitivi'

class PiTiVi(N):
    __doc__ = _('PiTiVi: Movie editor')
    license = LGPL + ' http://www.pitivi.org/'
    category = 'media'
    if UBUNTU or MINT:
        pkgs = 'pitivi'

class PowerTop(N):
    'PowerTop'
    detail = _('Powertop helps you save power for your laptop.')
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'powertop'
        
class QCad(N):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    license = GPL
    category = 'em'
    if FEDORA:
        pkgs = 'qcad'

class QCad(N):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    detail = ''
    category = 'em'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'qcad'
        
class QT_Creator(N):
    'Qt Creator'
    detail = _('This is an IDE for Qt.')
    category = 'dev'
    license = GPL
    if FEDORA:
        pkgs = 'qt-creator'

class QT_Creator(N):
    'Qt Creator'
    detail = _('This is an IDE for Qt.')
    category = 'dev'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'qtcreator qt4-dev-tools qt4-doc qt4-qtconfig'

class Qnapi(N):
    __doc__ = 'Qnapi'
    detail = _('QNapi is unofficial free clone of NAPI-PROJEKT program. '
                'Its purpose is to find and download subtitles for given video file. Currently only Polish subtitles are available.')
    license = GPL
    category = 'media'
    if UBUNTU or MINT:
        pkgs = 'qnapi'
        def visible(self):
            return Config.is_Poland_locale()

class QtiPlot(N) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.')
    category = 'math'
    license = GPL
    if FEDORA:
        pkgs = 'qtiplot'

class QtiPlot(N) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.')
    category = 'math'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'qtiplot'

class R_Language_Basic(N):
    __doc__ = _('R language (basic development environment)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/')
    category = 'statistics'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'r-base-core'

class R_Language_Full(N):
    __doc__ = _('R language (full development environment and all plugins)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/')
    category = 'statistics'
    license = GPL
    if UBUNTU or MINT:
        def __init__(self):
            import StringIO
            value = StringIO.StringIO()
            print >>value, 'r-base-core',
            for p in APT.get_existing_pkgs_set():
                if p.startswith('r-cran-'): print >>value, p,
            self.pkgs = value.getvalue()

class SDL(N):
    __doc__ = _('SDL library')
    detail = _('This is a library for writing SDL programs.\n'
               'SDL is a cross-platform multimedia library designed to provide low level access to audio'
               ' keyboard, mouse, joystick, 3D hardware via OpenGL, and 2D video framebuffer.')
    category = 'dev'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = 'libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev'

class ScienceBiology(N):
    __doc__ = _('Med-bio: A lot of micro-biology software')
    detail = _('A lot of software for molecular biology, structural biology and bioinformatics.')
    category = 'biology'
    license = DUAL_LICENSE(EPL, GPL)
    if UBUNTU or MINT:
        pkgs = 'med-bio'

class Screenlets(N):
    __doc__ = _('Screenlets: Add eye candy gadgets on desktop')
    detail = _('Screenlets is able to add eye candy gadgets on desktop, '
       'such as sticky notes, clocks, weather forecasts, calendars and so on, '
       'in order to decorate the desktop.')
    category = 'appearance'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'screenlets'

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

class StartupManager(N):
    __doc__ = _('Startup Manager: Change GRUB settings and themes')   
    detail = _('Startup manager helps you change GRUB settings and themes.')
    license = GPL
    category = 'appearance'
    if UBUNTU or MINT:
        pkgs = 'startupmanager'
        
class Svn_Git_bzr(N):
    __doc__ = _('Subversion, Git and Bzr: Popular version control systems')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'subversion git-core bzr'
        
class TeXLive2007(N):
    'TeXLive 2007'
    category = 'latex'
    if UBUNTU or MINT:
        pkgs = 'texlive'
class TuxPaint(N):
    __doc__ = _('Tux Paint: A drawing program for young children three years and up')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'tuxpaint'

class TuxPaint(N):
    __doc__ = _('Tux Paint: A drawing program for young children three years and up')
    category = 'education'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'tuxpaint'

class Typespeed(N) :
    'Typespeed'
    detail= _('Typespeed is a typing practise. It only runs in terminal.')
    category = 'game'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = "typespeed"

class Ubuntu_Studio_Theme(N):
    __doc__ = _('Ubuntu Studio Theme')
    license = GPL
    category = 'appearance'
    if UBUNTU or MINT:
        pkgs = 'ubuntustudio-theme ubuntustudio-icon-theme ubuntustudio-wallpapers ubuntustudio-gdm-theme'
    
class Umbrello(N):
    __doc__ = _('Umbrello: UML modelling')
    detail = _('Umbrello help you do UML modelling.')
    license = GPL
    category = 'dev'
    if UBUNTU or MINT:
        pkgs = 'umbrello'

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

class VirtualBox(N):
    __doc__ = _('VirtualBox open source edition')
    detail = _('It is the only professional virtual machine which is freely available '
       'under the terms of GPL. '
       'Official site: http://www.virtualbox.org/wiki/Downloads')
    license = GPL
    category = 'vm'
    if UBUNTU or MINT:
        pkgs = 'virtualbox-ose'

class Vuze_Karmic(N):
    # Latest Vuze is in 9.10 repository.
    __doc__ = _('Vuze: Download via bittorrent; Search videos')
    category = 'internet'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'vuze'
        def visible(self):
            return VERSION not in ['hardy', 'intrepid', 'jaunty']

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

class WorldofPadman(N):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.\n'
               'Download from ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/')
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'game'
    if FEDORA:
        pkgs = 'worldofpadman'

class Zhcon(N):
    __doc__ = _('Zhcon')
    detail = _('Zhcon helps you display Chinese characters in TTY terminal.\n'
               'You can launch it by "zhcon --utf8".')
    Chinese = True
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'zhcon'
