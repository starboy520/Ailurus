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

class Varkon(_apt_install, _path_lists):
    __doc__ = _('Varkon: A concise CAD software')
    detail = ( _('Be good at geometric modeling. '
                 'Please study the documentation '
                 '<span color="blue"><u>http://varkon.sourceforge.net/man.htm</u></span> before using it. ') +
               _(u'Developed by Örebro university, Sweden.') )
    category = 'em'
    license = GPL
    pkgs = 'varkon-user-manual varkon'
    def __init__(self):
        self.shortcut = '/usr/share/applications/varkon.desktop'
        self.paths = [ self.shortcut ]
    def install(self):
        _apt_install.install(self)
        create_file(self.shortcut, '''[Desktop Entry]
Name=Varkon
Exec=/usr/bin/varkon
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering;''')
    def installed(self):
        return _apt_install.installed(self)
    def remove(self):
        _apt_install.remove(self)
        run_as_root('rm -f %s'%self.shortcut)

class QCad(_apt_install):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    detail = ''
    category = 'em'
    license = GPL
    pkgs = 'qcad'
        
class Moonlight(_apt_install):
    __doc__ = _(u'Moonlight: an open source implementation of Microsoft® Silverlight')
    detail = _(u'Moonlight provides Windows® media codecs. '
       u'By this application, you can enjoy Windows® video/audio in webpages.')
    license = ('Moonlight 2.0 is licensed under LGPL and MIT X11 licenses. '
               'Moonlight 1.0 is licensed under LGPL. '
               'See http://www.mono-project.com/Moonlight')
    category = 'media'
    pkgs = 'moonlight-plugin-mozilla'

class DisableGetty(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def support(self):
        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty']
    def installed(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                if file_contain('tty%s'%i, 'start on runlevel 2'):
                    return False
            return True
    def install(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                filename = 'tty%s'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line=='start on runlevel 2\n':
                            contents[j]='stop on runlevel 2\n'
                        elif line=='start on runlevel 3\n':
                            contents[j]='stop on runlevel 3\n'
                    with open(filename, 'w') as f:
                        f.writelines(contents)
    def remove(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                filename = 'tty%s'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line=='stop on runlevel 2\n':
                            contents[j]='start on runlevel 2\n'
                        elif line=='stop on runlevel 3\n':
                            contents[j]='start on runlevel 3\n'
                    with open(filename, 'w') as f:
                        f.writelines(contents)

class DisableGettyKarmic(DisableGetty):
    __doc__ = DisableGetty.__doc__
    def support(self):
        return Config.get_Ubuntu_version() in ['karmic']
    def installed(self):
        with Chdir('/etc/init/') as o:
            for i in range(2,7):
                if file_contain('tty%s.conf'%i, 'exec /sbin/getty -8 38400 tty%s'%i):
                    return False
            return True
    def install(self):
        with Chdir('/etc/init/') as o:
            for i in range(2,7):
                filename = 'tty%s.conf'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line.strip()=='exec /sbin/getty -8 38400 tty%s'%i:
                            contents[j]='#exec\n'
                            break
                    else:
                        raise CommandFailError('Not found', contents)
                    with open(filename, 'w') as f:
                        f.writelines(contents)
    def remove(self):
        with Chdir('/etc/init/') as o:
            for i in range(2,7):
                filename = 'tty%s.conf'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line=='#exec\n':
                            contents[j]='exec /sbin/getty -8 38400 tty%s\n'%i
                            break
                    else:
                        raise CommandFailError('Not found', contents)
                    with open(filename, 'w') as f:
                        f.writelines(contents)

class Octave(_apt_install):
    __doc__ = _(u'Octave: A Matlab® compatible numerical computation appliation')
    license = GPL
    category = 'math'
    pkgs = 'qtoctave'
    def remove(self):
        _apt_install.remove(self)
        run_as_root('apt-get remove octave* -qq')

class Generic_Genome_Browser(I):
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>') 
    category='biology'
    license = AL
    def install(self):
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        run_as_root_in_terminal('perl %s' % f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError

class Screenlets(_apt_install):
    __doc__ = _('Screenlets: Add eye candy gadgets on desktop')
    detail = _('Screenlets is able to add eye candy gadgets on desktop, '
       'such as sticky notes, clocks, weather forecasts, calendars and so on, '
       'in order to decorate the desktop.')
    category = 'appearance'
    license = GPL
    pkgs = 'screenlets'

class CompizSettingManager(_apt_install):
    __doc__ = _('Compiz settings manager')
    detail = _('Compiz Fusion is the unification of the Beryl project and the community around the Compiz Window Manager. '
       'Compiz settings manager is the configuration application for Compiz Fusion. '
       'It can configurate effects such as "Desktop cube" and "3D windows".')
    category = 'appearance'
    license = GPL
    pkgs = 'compizconfig-settings-manager'

class CompizSettingManagerSimple(_apt_install):
    __doc__ = _('Simple-ccsm: A simple Compiz settings manager')
    category = 'appearance'
    license = GPL
    pkgs = 'simple-ccsm'

class ScienceBiology(_apt_install):
    __doc__ = _('Med-bio: A lot of micro-biology software')
    detail = _('A lot of software for molecular biology, structural biology and bioinformatics.')
    category = 'biology'
    license = DUAL_LICENSE(EPL, GPL)
    pkgs = 'med-bio'

class TuxPaint(_apt_install):
    __doc__ = _('Tux Paint: A drawing program for young children three years and up')
    category = 'education'
    license = GPL
    pkgs = 'tuxpaint'

class CodeBlocks(_apt_install):
    __doc__ = _('Code::Blocks - C/C++ IDE')
    license = GPL
    category = 'dev'
    pkgs = 'codeblocks'

class ChildsPlay(_apt_install):
    __doc__ = _('ChildsPlay: A suite of educational games for children')
    category = 'education'
    license = GPL
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
        
class GCompris(_apt_install):
    __doc__ = _('GCompris: Educational games for children aged 2 to 10')
    category = 'education'
    license = GPL
    def __init__(self):
        pkgs = APT.get_existing_pkgs_set()
        voices = [ e for e in pkgs if e.startswith('gcompris-sound-') ]
        lang = Config.get_locale().split('_')[0]
        voice = 'gcompris-sound-'+lang
        if not voice in voices: voice = ''
        else: voice = ' ' + voice
        self.pkgs = 'gnucap gcompris' + voice
 
class QT_Creator(_apt_install):
    'Qt Creator'
    detail = _('This is an IDE for Qt.')
    category = 'dev'
    license = GPL
    pkgs = 'qtcreator qt4-dev-tools qt4-doc qt4-qtconfig'

class Kadu(_apt_install):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.')
    category = 'internet'
    pkgs = 'kadu'
    def support(self):
        return Config.is_Poland_locale()

class Qnapi(_apt_install):
    __doc__ = 'Qnapi'
    detail = _('QNapi is unofficial free clone of NAPI-PROJEKT program. '
                'Its purpose is to find and download subtitles for given video file. Currently only Polish subtitles are available.')
    license = GPL
    category = 'media'
    pkgs = 'qnapi'
    def support(self):
        return Config.is_Poland_locale()

#class Audacious(_apt_install):
#    __doc__ = 'Audacious'
#    detail = _('Audacious is a media player which supports many media formats and third-party plugins.')
#    category = 'media'
#    pkgs = 'audacious'    

#class Miro(_apt_install):
#    __doc__ = 'Miro'
#    detail = _("Miro is a free and Internet TV application.")
#    category = 'media'
#    pkgs = 'miro'

#class VLC(_apt_install):
#    __doc__ = 'VLC'
#    detail = _("VLC is a media player which supports many media formats.")
#    category = 'media'
#    pkgs = 'vlc'

class Parcellite(_apt_install):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = GPL
    pkgs = 'parcellite'
    def support(self):
        return not ( Config.get_Ubuntu_version() in ['hardy'] )

class R_Language_Basic(_apt_install):
    __doc__ = _('R language (basic development environment)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/')
    category = 'statistics'
    license = GPL
    pkgs = 'r-base-core'

class R_Language_Full(_apt_install):
    __doc__ = _('R language (full development environment and all plugins)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/')
    category = 'statistics'
    license = GPL
    def __init__(self):
        import StringIO
        value = StringIO.StringIO()
        print >>value, 'r-base-core',
        for p in APT.get_existing_pkgs_set():
            if p.startswith('r-cran-'): print >>value, p,
        self.pkgs = value.getvalue()

class Bluefish(_apt_install):
    __doc__ = _('Bluefish: Edit HTML web-pages')
    license = GPL
    category = 'dev'
    pkgs = 'bluefish'

class _tasksel(I):
    category = 'server'
    def install(self):
        Tasksel.install(self.name)
    def installed(self):
        return Tasksel.installed(self.name)
    def remove(self):
        Tasksel.remove(self.name)
    def support(self):
        return Tasksel.exists(self.name)
    def installation_command(self):
        return _('Command:') + ' sudo tasksel install ' + self.name

class Tasksel_LAMP_server(_tasksel):
    __doc__ = _('LAMP: Install Apache2 + MySQL + PHP')
    name = 'lamp-server'

class Tasksel_DNS_server(_tasksel):
    __doc__ = _('DNS server')
    name = 'dns-server'

class Tasksel_Mail_server(_tasksel):
    __doc__ = _('Mail server')
    name = 'mail-server'

class Tasksel_Openssh_server(_tasksel):
    __doc__ = _('OpenSSH server')
    name = 'openssh-server'

class Tasksel_Postgresql_server(_tasksel):
    __doc__ = _('PostgreSQL server')
    name = 'postgresql-server'

class Tasksel_Print_server(_tasksel):
    __doc__ = _('Printer server')
    name = 'print-server'

class Tasksel_Samba_server(_tasksel):
    __doc__ = _('Samba file sharing server')
    name = 'samba-server'

class Tasksel_Tomcat_server(_tasksel):
    __doc__ = _('Tomcat Java server')
    name = 'tomcat-server'

class Tasksel_Ubuntustudio_graphics(_tasksel):
    __doc__ = _('Ubuntustudio-graphics: 2D/3D creation and editing')
    name = 'ubuntustudio-graphics'

class Tasksel_Ubuntustudio_audio(_tasksel):
    __doc__ = _('Ubuntustudio-audio: Audio creation and editing')
    name = 'ubuntustudio-audio'

class Tasksel_Ubuntustudio_audio_plugins(_tasksel):
    __doc__ = _('Ubuntustudio-audio-plugins: LADSPA and DSSI audio creation and editing')
    name = 'ubuntustudio-audio-plugins'

class Tasksel_Mobile_MID(_tasksel):
    __doc__ = _('Ubuntu MID')
    name = 'mobile-mid'

class Tasksel_Mobile_netbook_remix(_tasksel):
    __doc__ = _('Ubuntu Netbook')
    name = 'mobile-netbook-remix'

class Tasksel_Ubuntustudio_video(_tasksel):
    __doc__ = _('Ubuntustudio-video: Video creation and editing')
    name = 'ubuntustudio-video'

class Tasksel_Mobile_Live(_tasksel):
    __doc__ = _('Ubuntu MID Live')
    name = 'mobile-live'

class Tasksel_Eucalyptus_simple_cluster(_tasksel):
    __doc__ = _('Eucalyptus cloud computing cluster')
    name = 'eucalyptus-simple-cluster'
        
class Tasksel_Eucalyptus_node(_tasksel):
    __doc__ = _('Eucalyptus cloud computing node')
    name = 'eucalyptus-node'

class Tasksel_UEC(_tasksel):
    __doc__ = _('Ubuntu Enterprise Cloud server')
    name = 'uec'

class Tasksel_Ubuntustudio_font_meta(_tasksel):
    __doc__ = _('Ubuntustudio-font-meta: A lot of font')
    name = 'ubuntustudio-font-meta'

class Launch_Tasksel(I):
    __doc__ = _('* Launch tasksel')
    detail = _('This is a helper item. It just launches command: "sudo tasksel". '
               'Then you are free to customize your computer via "tasksel".')
    category = 'server'
    def installed(self):
        return False
    def install(self):
        if not APT.installed('tasksel'): APT.install('tasksel')
        run_as_root_in_terminal('tasksel')
        APT.cache_changed()
    def remove(self):
        raise NotImplementedError

class Fcitx(I):
    'Fcitx'
    category = 'language'
    detail = _('This is a popular Chinese input method.\n'
               'It is from http://fcitx.googlecode.com/')
    Chinese = True
    license = GPL
    def install(self):
        if get_arch() == 32:
            f = R(['http://fcitx.googlecode.com/files/fcitx-svn_3.6.3-20100305-r309_i386.deb'],
                7377508,'bb5deee1dc997ce72c8be22b4d90c6fef1210b46').download()
        else:
            f=R(['http://fcitx.googlecode.com/files/fcitx-svn_3.6.3-20100305-r309_amd64.deb'],
                7408298,'00e9508a6602f71495e21222c204d14289ff0f13').download()
        run('gdebi-gtk ' + f)
        APT.cache_changed()
    def installed(self):
        return APT.installed('fcitx-svn')
    def remove(self):
        APT.remove('fcitx-svn')
        
class Vuze_Karmic(_apt_install):
    # Latest Vuze is in 9.10 repository.
    __doc__ = _('Vuze: Download via bittorrent; Search videos')
    category = 'internet'
    license = GPL
    pkgs = 'vuze'
    def support(self):
        return Config.get_Ubuntu_version() not in ['hardy', 'intrepid', 'jaunty']

class ImageMagick(_apt_install):
    __doc__ = _('ImageMagick: Edit images')
    detail = _('You can start it by /usr/bin/display')
    category = 'media'
    pkgs = 'imagemagick'
        
class PiTiVi(_apt_install):
    __doc__ = _('PiTiVi: Movie editor')
    license = LGPL + ' http://www.pitivi.org/'
    category = 'media'
    pkgs = 'pitivi'
