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

class CommonUsedProgrammingPackages(_apt_install):
    __doc__ = _('Useful applications for programming')
    detail = _('The tools are:\n'
       '<i>'
       'g++: GNU C++ compiler.\n'
       'manpages-dev: manual pages about Linux system calls and library calls.\n'
       'manpages-posix: manual pages about using POSIX.\n'
       'manpages-posix-dev: manual pages about POSIX header files and POSIX library files.\n'
       'exuberant-ctags: source code parser used in vi and emacs, which allow moving to the definition of a symbol.\n'
       'libgmp3: GNU multiprecision arithmetic library.\n'
       'libncurses5: a library controlling writing to the console screen.\n'
       'libqt3-mt: Trolltech Qt library, version 3.\n'
       'subversion: a version control system.\n'
       'git-core: a distributed version control system.\n'
       '</i>'
       'Command: sudo apt-get install '
       'build-essential manpages-dev manpages-posix manpages-posix-dev exuberant-ctags '
       'libgmp3-dev libncurses5-dev libqt3-mt-dev subversion git-core')
    category = 'dev'
    time = 55
    size = 30988 * 1000
    logo = 'program-tools.png'
    def __init__(self):
        # Do not put 'libgmp3c2' in self.pkgs, or a lot of packages will be removed!
        # Besides, libgmp3-dev depends on 'libgmp3c2'. 'libgmp3c2' is not needed.   
        self.pkgs = ( "build-essential manpages-dev manpages-posix-dev manpages-posix exuberant-ctags" +
                      " libgmp3-dev libncurses5-dev libqt3-mt-dev subversion git-core" )
    def get_reason(self, f):
        self._get_reason(f)

class VirtualBox:
    'SUN® VirtualBox 3'
    detail = _('It is the only professional virtual machine which is freely available '
       'under the terms of GPL. '
       'Official site: http://www.virtualbox.org/wiki/Downloads')
    category = 'vm'
    time = 63
    size = 89372 * 1000
    manual = True
    logo = 'virtualbox.png'
    def install(self):
        if not APT.installed('build-essential'):
            print _(' "build-essential" is required. It is to be installed.')
            APT.install('build-essential')

        if Config.get_Ubuntu_version()=='hardy':
            if get_arch()==32:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_hardy_i386.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_hardy_i386.deb'],
57410500, '1282703ec6bcdd0b12c3eb277bb538b0da0ece04').download()

            else:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_hardy_amd64.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_hardy_amd64.deb'],
55999400, 'be76c44208b0ea98f2bd552d78ee2ef99e01cf85').download()
        
        elif Config.get_Ubuntu_version()=='intrepid':
            if get_arch()==32:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_intrepid_i386.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_intrepid_i386.deb'],
44069530, '6fefafb7df8bd2d81d7f631484fc9676cb8a411e').download()

            else:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_intrepid_amd64.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_intrepid_amd64.deb'],
44565230, 'ce6a68cb6a0fe0cbe95eb86020a816cae7f55dd0').download()

        elif Config.get_Ubuntu_version()=='jaunty':
            if get_arch()==32:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_jaunty_i386.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_jaunty_i386.deb'],
44074176, '5022b94456e24b6e099b366addd8e56bcfc6a261').download()

            else:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_jaunty_amd64.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_jaunty_amd64.deb'],
44562882, '4be3170ad1a29445d4f57071e08c14a5aeaa3c8e').download()

        elif Config.get_Ubuntu_version()=='karmic':
            if get_arch()==32:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_karmic_i386.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_karmic_i386.deb'],
43774454, '5a965a387806edacdbedd20347b9cf7b85ea62b4').download()

            else:
                f=R(
['http://tdt.sjtu.edu.cn/S/Virtualbox/virtualbox-3.0_3.0.12-54655_Ubuntu_karmic_amd64.deb',
'http://download.virtualbox.org/virtualbox/3.0.12/virtualbox-3.0_3.0.12-54655_Ubuntu_karmic_amd64.deb'],
43893164, '02b133a37c906b57ebe8c8176a3388c6ff272929').download()

        gksudo('gdebi-gtk %s'%f)        # do not use gdebi !
        APT.cache_changed()
    def installed(self):
        return APT.installed('virtualbox-3.0')
    def remove(self):
        APT.remove('virtualbox-3.0')

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
