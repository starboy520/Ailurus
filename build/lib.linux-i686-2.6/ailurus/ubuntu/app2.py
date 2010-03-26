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
from third_party_repos import _repo

class _repo_mplayer_vod(_repo):
    def __init__(self):
        self.desc = 'mplayer_vod'
        self.apt_content = 'mplayer'
        self.web_page = 'https://launchpad.net/~homer-xing/+archive/mplayer-vod'
        self.apt_file = '/etc/apt/sources.list.d/mplayer-vod.list'
        self.apt_conf = [ 'deb http://ppa.launchpad.net/homer-xing/mplayer-vod/ubuntu $version main' ]
        self.key_url = 'http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0xFDC8AE7E17C96D481FEA0410D10C093AFFA63A31'
        self.key_id = 'FFA63A31'
        _repo.__init__(self)

class ComicVODPlayer_new :
    __doc__ = _('Mplayer with "vod" protocol support')
    detail = _('Install mplayer and comicview. Mplayer supports "vod" protocol. "vod" protocol is used in some online video sites such as SJTU comic.')
    category = 'media'
    Chinese = True
    logo = 'comic.png'
    def install(self):
        # install comicview
        extension_path = FirefoxExtensions.get_extensions_path()
        comicview = R(['http://ailurus.googlecode.com/files/comicview-0.2.8.xpi']).download()
        run('cp %s %s'%(comicview, extension_path) )
        delay_notify_firefox_restart()
        
        # install mplayer-vod
        repo = _repo_mplayer_vod()
        if not repo.installed():
            repo.install()
        APT.apt_get_update()
        run('sudo apt-get install mplayer')
    def installed(self):
        return False
    def remove(self):
        raise NotImplemented

class PBC:
    __doc__ = _('PBC (Pairing-Based Cryptography) library')
    detail = ( _('Install Pairing-Based Cryptography library, powered by Stanford University.\n') +
               _('Official site: <span color="blue"><u>http://crypto.stanford.edu/pbc/</u></span> .') )
    category = 'dev'
    time = 30
    size = ( 300 + 808 ) * 1000
    logo = 'pbc.png'
    def install(self):
        if get_arch()==32:
            fdev=R(
['http://voltar.org/pbcfiles/libpbc-dev_0.5.4-1_i386.deb'],
182700, 'f2493c4c8ad0515babf28b1c5241583d993ad169'
).download()
        else:
            fdev=R(
['http://voltar.org/pbcfiles/libpbc-dev_0.5.4-1_amd64.deb'],
206752, '6ebfb58ddb53f8c63c475f871f843e2e5c2ec676'
).download()

        if get_arch()==32:
            f=R(
['http://voltar.org/pbcfiles/libpbc0_0.5.4-1_i386.deb'],
87122, '4424b14adee23683eff979c4efe33f493f2d2a55'
).download()
        else:
            f=R(
['http://voltar.org/pbcfiles/libpbc0_0.5.4-1_amd64.deb'],
96028, 'db19a612666605a18db319976b92c492e5371b91'
).download()

        DPKG.install_deb(f, fdev)
        
    def installed(self):
        return APT.installed('libpbc0') and APT.installed('libpbc-dev')
    
    def remove(self):
        APT.remove('libpbc0', 'libpbc-dev')
   
class Build_Essential(_apt_install):
    'Build-Essential'
    detail = _('Build-Essential is a c/c++ develop package. It contains gcc,make,gdb,libc and so on.\n'
            'Command: sudo apt-get install build-essential')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'build-essential'

class ManPages(_apt_install):
    'ManPages'
    detail = _('manpages-dev: manual pages about Linux system calls and library calls.\n'
               'manpages-posix: manual pages about using POSIX.\n'
               'manpages-posix-dev: manual pages about POSIX header files and POSIX library files.\n'
              'Command: sudo apt-get install manpages-dev manpages-posix manpages-posix-dev')      
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'manpages-dev manpages-posix manpages-posix-dev'

class ExuBerant(_apt_install):
    'Exuberant-ctags'
    detail = _('source code parser used in vi and emacs, which allow moving to the definition of a symbol.\n'
               'Command: sudo apt-get install exuberant-ctags')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'exuberant-ctags'

class LibgMp3Dev(_apt_install):
    'Libgmp3-dev'
    detail = _('GNU multiprecision arithmetic library.\n'
        'Command: sudo apt-get install libgmp3-dev')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'libmp3-dev'

class LibCurseQt(_apt_install):
    'libncurses5-dev And libqt3-mt-dev'
    detail = _('libncurses5: a library controlling writing to the console screen.\n'
       'libqt3-mt: Trolltech Qt library, version 3.\n' 
        'Command: sudo apt-get install libncurses5-dev libqt3-mt-dev')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'libncurses5-dev libqt3-mt-dev'
        
class SvnGit(_apt_install):
    'Subversion and  git-core'
    detail = _('subversion: a version control system.\n'
       'git-core: a distributed version control system.\n'
       'Command: sudo apt-get install subversion git-core.')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'subversion git-core'
        
class AutoTools(_apt_install):
    __doc__ = _('Tools for AutoMake')
    detail = _('autoconf: an package that produce shell scripts to automatically configure software source code packages.\n'
               'automake: a tool for automatically generating Makefile.\n'
               'Command: sudo apt-get install autoconf automake autotool')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'autotool autoconf automake'
        
class FreegLut3(_apt_install):
    __doc__ = _('FreeLut3: OpenGL Utility Toolkit')  
    detail = _('GLUT is a window system independent toolkit for writing OpenGL programs.\n'
                'Command: sudo apt-get install freeglut3-dev') 
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'freeglut3-dev'
        
class LibBoost(_apt_install):
    'LibBoost'
    detail = _('Boost C++ Libraries development files.\n'
        'Command: sudo apt-get install libboost-dev')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = 'libboost-dev'

class LibSDL(_apt_install):
    __doc__ = _('Simple DirectMedia Layer')
    detail = _('cross-platform multimedia library designed to provide low level access to audio'
               ' keyboard, mouse, joystick, 3D hardware via OpenGL, and 2D video framebuffer.\n'
               'Command: sudo apt-get install libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev')
    def __init__(self):
        self.pkgs = 'libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev'
    category = 'dev'
    logo = 'program-tools.png'
    
class PipeViewer(_apt_install):
    'Pipe Viewer'
    detail = _('A terminal-based tool for monitoring the progress of data through a pipeline.\n'
        'Command: sudo apt-get install pv')
    def __init__(self):
        self.pkgs = 'pv'
          
class AutoApt(_apt_install):
    'Auto-Apt'
    detail = _('Usage: "auto-apt run ./configure" can help you to find  the package is not installed.\n'
        'Command: sudo apt-get install auto-apt')
    def __init__(self):
        self.pkgs = 'auto-apt'

class CheckInstall(_apt_install):
    'CheckInstall'
    detail = _('Can replace the "make install" to achieve the source code installed as a deb, to achieve package management.\n'
         'Command: sudo apt-get install checkinstall')
    def __init__(self):
        self.pkgs = 'checkinstall'
        
class Umbrello(_apt_install):
    __doc__ = _('Umbrello: An UML Modeller')
    detail = _('Umbrello: allows you to create diagrams of software and other systems in a standard format.\n'
            'Command: sudo apt-get install umbrello')
    def __init__(self):
        self.pkgs = 'umbrello'
    category = 'dev'
    logo = 'program-tools.png'

class Ubuntu_Theme(_apt_install):
    'Ubuntu Studio Theme'
    detail = _('Command: sudo apt-get install ubuntustudio-theme ubuntustudio-icon-theme ubuntustudio-wallpapers ubuntustudio-gdm-theme')
    def __init__(self):
        self.pkgs = 'ubuntustudio-theme ubuntustudio-icon-theme ubuntustudio-wallpapers ubuntustudio-gdm-theme'
    
class MiniCom_Ckermit(_apt_install):
    'MiniCom And Ckermit'
    detail = _('minicom: a clone of the MS-DOS "Telix" communication program.\n'
                'ckermit: combined serial and network communication software package.\n'
                'Command: sudo apt-get install minicom ckermit')
    def __init__(self):
        self.pkgs = 'minicom ckermit'

class VirtualBox:
    'SUN® VirtualBox 3'
    detail = _('It is the only professional virtual machine which is freely available '
       'under the terms of GPL. '
       'Official site: http://www.virtualbox.org/wiki/Downloads')
    category = 'vm'
    manual = True
    logo = 'virtualbox.png'
    def install(self):
        from third_party_repos import Repo_VirtualBox
        vbox_obj = Repo_VirtualBox()
        if not vbox_obj.installed(): vbox_obj.install()
        APT.apt_get_update()
        APT.install('virtualbox-3.1')
    def installed(self):
        for p in ['virtualbox-3.1', 'virtualbox-3.0', 'virtualbox-2.2', 'virtualbox-2.1', 'virtualbox-2.0', 'virtualbox']:
            if APT.installed(p): return True
        return False
    def remove(self):
        for p in ['virtualbox-3.1', 'virtualbox-3.0', 'virtualbox-2.2', 'virtualbox-2.1', 'virtualbox-2.0', 'virtualbox']:
            if APT.installed(p): APT.remove(p)

class GNOMEArtNextGen:
    __doc__ = _('GNOMEArtNG')
    detail = _('It is able to customize the backgrounds, application look, window borders, icons, GNOME splash and GDM window. '
       'More than 100 themes can be installed, which are downloaded from http://art.gnome.org . '
       'The official site of GNOMEArtNG is http://developer.berlios.de/projects/gnomeartng/')
    category = 'appearance'
    size = 225 * 1000
    logo = 'gnomeartng.png'
    def install(self):
        if Config.get_Ubuntu_version() == 'hardy':

            file = R(
['http://tdt.sjtu.edu.cn/S/gnomeartng-0.7.0-hardy.deb',
'http://download.berlios.de/gnomeartng/gnomeartng-0.7.0-hardy.deb'],
471212, '52c556fafa9664284dcff9851528f3e5aae00ebe').download()
        
        elif Config.get_Ubuntu_version() == 'intrepid':
        
            file = R(
['http://tdt.sjtu.edu.cn/S/gnomeartng-0.7.0-intrepid.deb',
'http://download.berlios.de/gnomeartng/gnomeartng-0.7.0-intrepid.deb'],
444822, '4dc42fd446ebd8e615cf6490d6ecc94a403719b8').download()
        
        elif Config.get_Ubuntu_version() == 'jaunty':
        
            file = R(
['http://tdt.sjtu.edu.cn/S/gnomeartng-0.7.0-jaunty.deb',
'http://download.berlios.de/gnomeartng/gnomeartng-0.7.0-jaunty.deb'],
441222, 'c9134ad3405c660e6e07333994ca38d494f0f90f').download()
        
        elif Config.get_Ubuntu_version() == 'karmic':
        
            file = R(
['http://tdt.sjtu.edu.cn/S/gnomeartng-0.7.0-karmic.deb',
'http://ailurus.googlecode.com/files/gnomeartng-0.7.0-karmic.deb',],
441558, 'b2b834b1bfc76f01dce370b60ea706f6ed35e4da').download()

        else:
            raise Exception('GNOMEArtNextGen', Config.get_Ubuntu_version())

        DPKG.install_deb(file)
        
        thumb = R(['http://download.berlios.de/gnomeartng/thumbs.tar.gz'],
           15575567, '7b7dcc3709d23383c1433f90abea5bea583202f9').download()
        import os
        path = os.path.expanduser('~/.gnome2/gnome-art-ng/')
        if not os.path.exists(path): run('mkdir '+path)
        with Chdir(path) as o:
            run('tar xf '+thumb)
    def installed(self):
        return APT.installed('gnomeartng')
    def remove(self):
        APT.remove('gnomeartng')
    def support(self):
        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty', 'karmic']

class QtiPlot(_apt_install) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.\n'
       'Command: sudo apt-get install qtiplot')
    category = 'math'
    size = 6064 * 1000
    logo = 'qtiplot.png'
    def __init__(self):
        self.pkgs = 'qtiplot'

class Extcalc(_apt_install):
    'Extcalc'
    detail = _('This is a multifunctional graphic calculator.\n'
        'Command: sudo apt-get install extcalc')
    category = 'math'
    logo = 'extcalc.png'
    def __init__(self):
        self.pkgs = 'extcalc'
        
class MacChanger(_apt_install):
    'Macchanger'
    detail = ('Macchanger is a GNU/Linux utility for viewing/manipulating the MAC address of network interfaces.\n'
        'Command: sudo apt-get install macchanger')
    def __init__(self):
        self.pkgs = 'macchanger'
        
class BlueTooth_Phone(_apt_install):
    'BlueTooth and Telephones'
    detail = _('Command: sudo apt-get install bluetooth bluez-alsa bluez-cups bluez-gnome bluez-utils python-bluez gnome-bluetooth gnome-phone-manager')
    def __init__(self):
        self.pkgs = 'bluetooth bluez-alsa bluez-cups bluez-gnome bluez-utils python-bluez gnome-bluetooth gnome-phone-manager'
        
class StartupManager(_apt_install):
    __doc__ = _('SatartupManager: Change settings and manage themes for Grub and Usplash.')   
    detail = _('Start Method: sudo startupmanager.\n'
      'Command: sudo apt-get install startupmanager')  
    def __init__(self):
        self.pkgs = 'startupmanager'
        
class Zhcon(_apt_install):
    __doc__ = _('Zhcon: a tool that enable you to input Chinese in your terminal')
    detail = _('Start Method: zhcon --utf8.\n'
         'Command: sudo apt-get install zhcon')
    def __init__(self):
        self.pkgs = 'zhcon'
        
class PowerTop(_apt_install):
    'PowerTop'
    detail = _('Powertop is a linux tool to find out what is using power on your laptop.\n'
        'Command: sudo apt-get install powertop')
    def __init__(self):
        self.pkgs = 'powertop'



