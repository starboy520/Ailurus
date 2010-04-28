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
from third_party_repos import *

class Acire(_apt_install):
    __doc__ = _('Acire: A Python code fragment manager')
    license = GPL
    category = 'dev'
    depends = Repo_Acire
    pkgs = 'acire'
    def support(self):
        return Config.get_Ubuntu_version() not in ['hardy', 'intrepid', 'jaunty']

class AWN(_apt_install):
    __doc__ = _('AWN (Avant Window Navigator): A dock-like bar')
    license = GPL
    category = 'appearance'
    depends = Repo_AWN_Development
    pkgs = 'avant-window-navigator-trunk'

class ComicView(_ff_extension):
    __doc__ = _('Adblock+: Block 99% advertisement')
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'http://ailurus.googlecode.com/files/comicview-0.2.8.xpi'
        self.range = '3.0~3.7'
        self.name = u'Comic Viewer'
        self.R = R(['http://ailurus.googlecode.com/files/comicview-0.2.8.xpi'])
        _ff_extension.__init__(self)
    def support(self):
        return False

class ComicVODPlayer_new(I):
    __doc__ = _('Mplayer with "vod" protocol support')
    detail = _('Install mplayer and comicview. Mplayer supports "vod" protocol. "vod" protocol is used in some online video sites such as SJTU comic.')
    category = 'media'
    Chinese = True
    license = GPL
    depends = Repo_Mplayer_VOD
    def __init__(self):
        self.comicview = ComicView()
    def install(self):
        if not self.comicview.installed():
            self.comicview.install()
        # Remove current mplayer. Then install a newer version.
        APT.remove('mplayer')
        APT.install('mplayer')
        # Remove repository
        Repo_Mplayer_VOD().remove()
    def installed(self):
        return self.comicview.installed() and APT.installed('mplayer')
    def remove(self):
        APT.remove('mplayer')
    def support(self):
        return APT.installed('firefox')

class Audacious(_apt_install):
    __doc__ = _('Audacious: Audio player')
    license = GPL
    category = 'media'
    depends = Repo_Audacious
    pkgs = 'audacious audacious-plugins'

class Blueman(_apt_install):
    __doc__ = _('Blueman: Graphical blue-tooth manager')
    license = GPL
    category = 'hardware'
    depends = Repo_Blueman
    pkgs = 'blueman'

class Christine(_apt_install):
    __doc__ = _('Christine: Media player')
    license = GPL
    category = 'media'
    depends = Repo_Christine
    pkgs = 'christine'

class Gmchess(_apt_install):
    __doc__ = _('Gmchess: Chinese chess game')
    license = GPL
    category = 'game'
    depends = Repo_Gmchess
    pkgs = 'gmchess'

class Chromium(_apt_install):
    __doc__ = _('Chromium: Web browser')
    license = BSD
    category = 'internet'
    depends = Repo_Chromium_Daily
    pkgs = 'chromium-browser'

class Exaile(_apt_install):
    __doc__ = _('Exaile: Audio player')
    license = GPL
    category = 'media'
    depends = Repo_Exaile
    pkgs = 'exaile'

class Gnome_global_menu(_apt_install):
    __doc__ = _('Global Menu: A globally shared menu bar')
    license = GPL
    category = 'appearance'
    depends = Repo_GlobalMenu
    pkgs = 'gnome-globalmenu'

class Gnome_color(_apt_install):
    __doc__ = _('GNOME colors themes')
    license = GPL
    category = 'appearance'
    depends = Repo_GNOMEColors
    pkgs = 'gnome-colors'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class Getting_things_gnome(_apt_install):
    __doc__ = _('Getting Things Gnome: GTD tool')
    license = GPL
    category = 'office'
    logo = 'gtg.png'
    depends = Repo_GTG
    pkgs = 'gtg'

class Moovida(_apt_install):
    __doc__ = _('Moovida: Media player')
    license = GPL
    category = 'media'
    depends = Repo_Moovida
    pkgs = 'moovida'

class OSD_Lyrics(_apt_install):
    __doc__ = _('OSD-Lyrics: Display lyrics')
    category = 'media'
    license = GPL
    depends = Repo_OSD_Lyrics
    pkgs = 'osdlyrics'

class Pidgin_beta(_apt_install):
    __doc__ = _('Pidgin (beta version)')
    license = GPL
    category = 'internet'
    depends = Repo_Pidgin_Develop
    pkgs = 'pidgin'
    def installed(self):
        if APT.installed('pidgin'):
            string = get_output('pidgin -v')
            version = string.split()[1]
            return tuple(map(int,version.split('.'))) >= (2, 6, 6)
        return False
    def install(self):
        if APT.installed('pidgin'):
            APT.remove('pidgin')
        APT.install('pidgin')

class PlayOnLinux(_apt_install):
    __doc__ = _('PlayOnLinux: A graphical front-end for wine')
    license = LGPL
    category = 'game'
    depends = Repo_PlayOnLinux
    pkgs = 'playonlinux'

class RSSOwl(_apt_install):
    __doc__ = _('RSSOwl: RSS feed reader')
    license = EPL
    category = 'internet'
    depends = Repo_RSSOwl
    pkgs = 'rssowl'

class RedNoteBook(_apt_install):
    __doc__ = _('RedNoteBook: A desktop diary application')
    license = GPL
    category = 'office'
    depends = Repo_RedNoteBook
    pkgs = 'rednotebook'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'
    
class Shutter(_apt_install):
    __doc__ = _('Shutter: A screen-shot application')
    license = GPL
    category = 'tweak'
    depends = Repo_Shutter
    pkgs = 'shutter'

#class Synapse(_apt_install):
#    __doc__ = _('Synapse: An instance messanger')
#    license = GPL
#    category = 'internet'
#    depends = Repo_Synapse
#    pkgs = 'synapse'
#    def support(self):
#        return Config.get_Ubuntu_version() != 'lucid'

# Hide it in Lucid. Since Firefox is 3.6.3 in Lucid.
class Firefox_3_6(_apt_install):
    __doc__ = _('Firefox 3.6')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    category = 'internet'
    depends = Repo_Firefox_3_6
    pkgs = 'firefox'
    def support(self):
        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty', 'karmic']

class XBMC(_apt_install):
    __doc__ = _('XBMC: Home entertainment system')
    category = 'media'
    license = GPL
    depends = Repo_XBMC
    pkgs = 'xbmc'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class Songbird(_apt_install):
    __doc__ = _('Songbird: Open source substitution of iTunes')
    category = 'media'
    license = GPL
    depends = Repo_Songbird
    pkgs = 'songbird'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class Netbeans(_apt_install):
    __doc__ = 'Netbeans'
    detail = (
              _('It is an open source IDE which supports several languages (C, C++, Java, Ruby, etc.)'
               ' and frameworks (J2SE, J2ME, etc.). '
               'Official site: http://netbeans.org/downloads/ .') +
              _(' This application depends on Java.') )
    category = 'dev'
    license = DUAL_LICENSE(CDDL, GPL) + ' http://netbeans.org/about/legal/license.html'
    pkgs = 'netbeans'

class TeXLive2007(_apt_install):
    'TeXLive 2007'
    category = 'latex'
    pkgs = 'texlive'
