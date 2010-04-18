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
    detail = _("Acire provides Python code fragments which outline how to do specific tasks.")
    license = GPL
    category = 'dev'
    depends = Repo_Acire
    pkgs = 'acire python-snippets'

class AWN(_apt_install):
    __doc__ = _('Avant Window Navigator')
    detail = _('Avant Window Navigator (Awn) is a dock-like bar which sits at the bottom of the screen. It has support for launchers, task lists, and third party applets.')
    license = GPL
    category = 'appearance'
    depends = Repo_AWN_Development
    pkgs = 'avant-window-navigator-trunk'

class ComicVODPlayer_new(I):
    __doc__ = _('Mplayer with "vod" protocol support')
    detail = _('Install mplayer and comicview. Mplayer supports "vod" protocol. "vod" protocol is used in some online video sites such as SJTU comic.')
    category = 'media'
    Chinese = True
    license = GPL
    depends = Repo_Mplayer_VOD
    def install(self):
        extension_path = FirefoxExtensions.get_extensions_path()
        comicview = R(['http://ailurus.googlecode.com/files/comicview-0.2.8.xpi']).download()
        run('cp %s %s'%(comicview, extension_path) )
        delay_notify_firefox_restart()
        # Remove current mplayer. Then install a newer version.
        APT.remove('mplayer')
        APT.install('mplayer')
    def installed(self):
        return False
    def remove(self):
        raise NotImplemented

class Audacious(_apt_install):
    __doc__ = _('Audacious (beta version)')
    detail = _('An advanced audio player.It focused on audio quality and supporting a wide range of audio codecs.')
    license = GPL
    category = 'media'
    depends = Repo_Audacious
    pkgs = 'audacious audacious-plugins'

class blueman(_apt_install):
    __doc__ = _('Blueman')
    detail = _('Blueman is a graphical blue-tooth manager')
    license = GPL
    category = 'hardware'
    depends = Repo_Blueman
    pkgs = 'blueman'

class christine(_apt_install):
    __doc__ = _('Christine')
    detail = _('Christine is a small media player.')
    license = GPL
    category = 'media'
    depends = Repo_Christine
    pkgs = 'christine'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class Gmchess(_apt_install):
    __doc__ = _('Gmchess')
    detail = _('This is a Chinese chess game.')
    license = GPL
    category = 'game'
    depends = Repo_Gmchess
    pkgs = 'gmchess'

class chromium(_apt_install):
    __doc__ = _('Chromium')
    detail = _('Chromium is the open source version of Google Chrome.')
    license = BSD
    category = 'internet'
    depends = Repo_Chromium_Daily
    pkgs = 'chromium-browser'

class exaile(_apt_install):
    __doc__ = _('Exaile')
    detail = _('A music manager and player for GTK+ written in Python.')
    license = GPL
    category = 'media'
    depends = Repo_Exaile
    pkgs = 'exiale'

class gnome_global_menu(_apt_install):
    __doc__ = _('Global Menu Bar')
    detail = _('GNOME Global Menu is the globally-shared menu bar of all applications.')
    license = GPL
    category = 'appearance'
    depends = Repo_GlobalMenu
    pkgs = 'gnoe-globalmenu'

class gnome_color(_apt_install):
    __doc__ = _('GNOME colors theme (stable)')
    detail = _('Seven full color-schemes available; Brave (Blue), Human (Orange), Wine (Red), Noble (Purple), Wise (Green), Dust (Chocolate) and Illustrious (Pink) will be installed.')
    license = GPL
    category = 'appearance'
    depends = Repo_GNOMEColors
    pkgs = 'arc-colors gnome-color shiki-colors-murrine'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class getting_things_gnome(_apt_install):
    __doc__ = _('Getting Things Gnome(Lastest version)')
    detail = _('"Getting things GNOME" is a simple, powerful and flexible organization tool.')
    license = GPL
    category = 'office'
    logo = 'gtg.png'
    depends = Repo_GTG
    pkgs = 'gtg'

class moovida(_apt_install):
    __doc__ = _('Moovida')
    detail = _('Moovida is a cross platform media player.')
    license = GPL
    category = 'media'
    depends = Repo_Moovida
    pkgs = 'moovida'

class OSD_Lyrics(_apt_install):
    __doc__ = _('OSD-Lyrics: Display lyrics. Supports many media players.')
    category = 'media'
    license = GPL
    depends = Repo_OSD_Lyrics
    pkgs = 'osdlyrics'

class pidgin_beta(_apt_install):
    __doc__ = _('Pdigin beta version')
    detail = _('A free chat client used by millions. Connect easily to MSN, Google Talk, Yahoo, AIM and other chat networks all at once.')
    license = GPL
    category = 'internet'
    depends = Repo_Pidgin_Develop
    pkgs = 'pidgin'

class PlayOnLinux(_apt_install):
    __doc__ = _('PlayOnLinux')
    detail =  _('PlayOnLinux is a front-end for wine. ''It helps to install Windows Games and softwares on Linux.')
    license = LGPL
    category = 'media'
    depends = Repo_PlayOnLinux
    pkgs = 'playonlinux'

class RSSOwl(_apt_install):
    __doc__ = _('RSSOwl')
    detail = _('RSSOwl is a free and powerful news feed reader. ')
    license = EPL
    category = 'internet'
    depends = Repo_RSSOwl
    pkgs = 'rssowl'

class RedNoteBook(_apt_install):
    __doc__ = _('RedNoteBook')
    detail = _('This is a desktop diary application.')
    license = GPL
    category = 'office'
    depends = Repo_RedNoteBook
    pkgs = 'rednotebook'
    
class shutter(_apt_install):
    __doc__ = _('Shutter')
    detail = _('Shutter is a powerfull screenshot program')
    license = GPL
    category = 'tweak'
    depends = Repo_Shutter
    pkgs = 'shutter'

class synapse(_apt_install):
    __doc__ = _('Synapse')
    detail = _('Synapse is an instant messager.')
    license = GPL
    category = 'internet'
    depends = Repo_Synapse
    pkgs = 'synapse'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class tor(_apt_install):
    __doc__ = _('Tor')
    detail = _('An open network that helps you defend against a form of network surveillance that threatens personal freedom and privacy, '
        'confidential business activities and relationships, and state security known as traffic analysis.')
    license = BSD
    category = 'internet'
    depends = Repo_Tor
    pkgs = 'tor privoxy vidalia'

class firefox_3_6(_apt_install):
    __doc__ = _('Firefox 3.6')
    detail = _('')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    category = 'internet'
    depends = Repo_Firefox_3_6
    pkgs = 'firefox-3.6-branding'
    def installed(self):
        return APT.installed('firefox-3.6-branding')
    def remove(self):
        APT.install('firefox-3.5-branding')
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class XBMC(_apt_install):
    __doc__ = _('XBMC: Home entertainment system')
    category = 'media'
    license = GPL
    depends = Repo_XBMC
    pkgs = 'xbmc'

class Songbird(_apt_install):
    __doc__ = _('Songbird: Open source substitution of iTunes')
    category = 'media'
    license = GPL
    depends = Repo_Songbird
    pkgs = 'songbird'

