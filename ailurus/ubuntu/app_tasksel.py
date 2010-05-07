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
