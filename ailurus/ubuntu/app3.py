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
from third_party_repos import *

class DisableGetty(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def visible(self):
        return VERSION in ['hardy', 'intrepid', 'jaunty']
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
    def visible(self):
        return VERSION in ['karmic']
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

class _tasksel(I):
    category = 'server'
    def install(self):
        Tasksel.install(self.name)
    def installed(self):
        return Tasksel.installed(self.name)
    def remove(self):
        Tasksel.remove(self.name)
    def visible(self):
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
