#coding: utf-8
#
# Ailurus - a simple application installer and GNOME tweaker
#
# Copyright (C) 2009-2010, Ailurus developers and Ailurus contributors
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
import gtk
import sys, os
from lib import *
from libu import *
from libsetting import *

class update_manager_setting(Set):
    @classmethod
    def f(cls):
        label = gtk.Label(_('the behavior of update manager:'))
        label.set_alignment(0, 0)
        o = GConfCheckButton(_('selected = pop up update manager window.\n'
                               'unselected = show updates in the notification area'), '/apps/update-notifier/auto_launch' )
        
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(gtk.Label( _('Interval (in days) when to check for update:') ), False)
        e = GConfNumericEntry('/apps/update-notifier/regular_auto_launch_interval', 1, 30)
        hbox.pack_start(e, False)
        
        vbox = gtk.VBox(False, 0)
        vbox.pack_start(label, False)
        vbox.pack_start(o, False)
        vbox.pack_start(hbox, False)
        
        return vbox
    
    @classmethod
    def visible(cls):
        try: import gconf
        except: return False
        else: return True
        
    title = _('Ubuntu update manager setting')
    category = 'update'