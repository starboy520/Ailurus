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
    license = 'GNU General Public License'
    category = 'dev'
    depends = Repo_Acire
    pkgs = 'acire python-snippets'

class AWN(_apt_install):
    __doc__ = _('Avant Window Navigator')
    detail = _('Avant Window Navigator (Awn) is a dock-like bar which sits at the bottom of the screen. It has support for launchers, task lists, and third party applets.')
    license = 'GNU General Public License'
    category = 'appearance'
    depends = Repo_AWN_Development
    pkgs = 'avant-window-navigator-trunk'

class Audacious(_apt_install):
    __doc__ = _('Audacious (beta version)')
    detail = _('An advanced audio player.It focused on audio quality and supporting a wide range of audio codecs.')
    license = 'GNU General Public License'
    category = 'media'
    depends = Repo_Audacious
    pkgs = 'audacious audacious-plugins'

class blueman(_apt_install):
    __doc__ = _('Blueman')
    detail = _('Blueman is a graphical blue-tooth manager')
    license = 'GNU General Public License'
    category = 'hardware'
    depends = Repo_Blueman
    pkgs = 'blueman'

class christine(_apt_install):
    __doc__ = _('Christine')
    detail = _('Christine is a small media player.')
    license = 'GNU General Public License (GPL)'
    category = 'media'
    depends = Repo_Christine
    pkgs = 'christine'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class Gmchess(_apt_install):
    __doc__ = _('Gmchess')
    detail = _('This is a Chinese chess game.')
    license = 'GNU General Public License (GPL)'
    category = 'game'
    depends = Repo_Gmchess
    pkgs = 'gmchess'

class chromium(_apt_install):
    __doc__ = _('Chromium')
    detail = _('Chromium is the open source version of Google Chrome.')
    license = 'BSD license, MIT License, LGPL, Ms-PL, MPL/GPL/LGPL tri-license'
    category = 'internet'
    depends = Repo_Chromium_Daily
    pkgs = 'chromium-browser'

class exaile(_apt_install):
    __doc__ = _('Exaile')
    detail = _('A music manager and player for GTK+ written in Python.')
    license = 'GNU General Public License (GPL)'
    category = 'media'
    depends = Repo_Exaile
    pkgs = 'exiale'

class gnome_global_menu(_apt_install):
    __doc__ = _('Global Menu Bar')
    detail = _('GNOME Global Menu is the globally-shared menu bar of all applications.')
    license = 'GNU General Public License (GPL)'
    category = 'appearance'
    depends = Repo_GlobalMenu
    pkgs = 'gnoe-globalmenu'

class gnome_color(_apt_install):
    __doc__ = _('GNOME colors theme (stable)')
    detail = _('Seven full color-schemes available; Brave (Blue), Human (Orange), Wine (Red), Noble (Purple), Wise (Green), Dust (Chocolate) and Illustrious (Pink) will be installed.')
    license = 'GNU General Public License (GPL)'
    category = 'appearance'
    depends = Repo_GNOMEColors
    pkgs = 'arc-colors gnome-color shiki-colors-murrine'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class getting_things_gnome(_apt_install):
    __doc__ = _('Getting Things Gnome(Lastest version)')
    detail = _('"Getting things GNOME" is a simple, powerful and flexible organization tool.')
    license = 'GNU General Pulic License (PGL)'
    category = 'office'
    logo = 'gtg.png'
    depends = Repo_GTG
    pkgs = 'gtg'

class moovida(_apt_install):
    __doc__ = _('Moovida')
    detail = _('Moovida is a cross platform media player.')
    license = 'GNU General Public Licence (GPL)'
    category = 'media'
    depends = Repo_Moovida
    pkgs = 'moovida'

class osd_lurics(_apt_install):
    __doc__ = _('OSD Lyrics')
    detail = _('It displays lyrics. It supports many media players.')
    license = 'GNU General Public License (GPL)'
    category = 'media'
    depends = Repo_OSD_Lyrics
    pkgs = 'osd-lyrics'

class pidgin_beta(_apt_install):
    __doc__ = _('Pdigin beta version')
    detail = _('A free chat client used by millions. Connect easily to MSN, Google Talk, Yahoo, AIM and other chat networks all at once.')
    license = 'GNU General Public License (GPL)'
    category = 'internet'
    depends = Repo_Pidgin_Develop
    pkgs = 'pidgin'

class PlayOnLinux(_apt_install):
    __doc__ = _('PlayOnLinux')
    detail =  _('PlayOnLinux is a front-end for wine. ''It helps to install Windows Games and softwares on Linux.')
    license = 'GNU Lesser General Public License (LGPL)'
    category = 'media'
    depends = Repo_PlayOnLinux
    pkgs = 'playonlinux'

class RSSOwl(_apt_install):
    __doc__ = _('RSSOwl')
    detail = _('RSSOwl is a free and powerful news feed reader. ')
    license = 'Eclipse Public License'
    category = 'internet'
    depends = Repo_RSSOwl
    pkgs = 'rssowl'

class RedNoteBook(_apt_install):
    __doc__ = _('RedNoteBook')
    detail = _('This is a desktop diary application.')
    license = 'GNU General Public License (GPL)'
    category = 'office'
    depends = Repo_RedNoteBook
    pkgs = 'rednotebook'
    
class shutter(_apt_install):
    __doc__ = _('Shutter')
    detail = _('Shutter is a powerfull screenshot program')
    license = 'GNU General Public License (GPL)'
    category = 'tweak'
    depends = Repo_Shutter
    pkgs = 'shutter'

class synapse(_apt_install):
    __doc__ = _('Synapse')
    detail = _('Synapse is an instant messager.')
    license = 'GNU General Public License (GPL)'
    category = 'internet'
    depends = Repo_Synapse
    pkgs = 'synapse'
    def support(self):
        return Config.get_Ubuntu_version() != 'lucid'

class tor(_apt_install):
    __doc__ = _('Tor')
    detail = _('An open network that helps you defend against a form of network surveillance that threatens personal freedom and privacy, '
        'confidential business activities and relationships, and state security known as traffic analysis.')
    license = 'BSD License'
    category = 'internet'
    depends = Repo_Tor
    pkgs = 'tor privoxy vidalia'

