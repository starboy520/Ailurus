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
import gtk
import sys, os
from lib import *
from ulib import *
from settinglib import *

def __change_kernel_swappiness():
    vbox = gtk.VBox()
    text_box = gtk.HBox(False)
    text_box.pack_start( gtk.Label( _('0 = Swap little mem to disk') ), False, False )
    text_box.pack_start( gtk.Label(), True, True, 30 )
    text_box.pack_start( gtk.Label( _('100 = Swap a lot of mem to disk') ), False, False )
    
    current_value = int( get_output('/sbin/sysctl -n vm.swappiness').strip() )
    adjustment = gtk.Adjustment(current_value, 0, 100, 10, 10, 0)
    def update(adjustment):
        new_value = round( adjustment.value, -1 )
        adjustment.set_value( new_value )
    adjustment.connect("value_changed", update)
    scale = gtk.HScale(adjustment)
    scale.set_digits(0)
    scale.set_value_pos(gtk.POS_BOTTOM)

    def apply(w, adjustment):
        new_value = int( adjustment.get_value() )
        new_line = 'vm.swappiness = %s' % new_value
        with TempOwn('/etc/sysctl.conf') as o:
            with open('/etc/sysctl.conf') as f:
                contents = f.readlines()
            for i, line in enumerate(contents):
                if line[0]=='#' or line=='\n': continue
                if 'vm.swappiness' in line:
                    contents[i] = new_line
                    break
            else:
                contents.append(new_line)
            with open('/etc/sysctl.conf', 'w') as f:
                f.writelines(contents)
        gksudo('/sbin/sysctl -p')
    
    apply_button = image_stock_button(gtk.STOCK_APPLY, _('Apply') )
    apply_button.connect('clicked', apply, adjustment)
    align_apply_button = gtk.HBox(False, 0)
    align_apply_button.pack_end(apply_button, False)
    
    vbox.pack_start(text_box, False, False)
    vbox.pack_start(scale, False, False)
    vbox.pack_start(align_apply_button, False, False)
    vbox.set_size_request(500, -1)
    align_vbox = gtk.Alignment(0, 0)
    align_vbox.add(vbox)
    return Setting(align_vbox, _('Change the tendency of swapping memory to disk'), ['memory'])

def __restart_network():
     def restart_network(w):
         try:
             import dbus
             bus = dbus.SystemBus()
             obj = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
             obj.sleep(dbus_interface='org.freedesktop.NetworkManager')
             obj.wake(dbus_interface='org.freedesktop.NetworkManager')
             if Config.is_Ubuntu() or Config.is_Mint():
                 notify(' ', _('Run command: ')+'/etc/init.d/networking restart')
                 gksudo('/etc/init.d/networking restart')
             notify(_('Information'), _('Network restarted successfully.'))
         except: pass
     button_restart_network = gtk.Button(_('Restart network').center(30))
     button_restart_network.connect('clicked', restart_network)
     button_restart_network.set_tooltip_text(_('These commands will be executed:\n'
               'dbus-send --system --dest=org.freedesktop.NetworkManager '
               '--type=method_call /org/freedesktop/NetworkManager '
               'org.freedesktop.NetworkManager.sleep\n'
               'dbus-send --system --dest=org.freedesktop.NetworkManager '
               '--type=method_call /org/freedesktop/NetworkManager '
               'org.freedesktop.NetworkManager.wake\n'
               'sudo /etc/init.d/networking restart'))
     align_bfm = gtk.Alignment(0, 0.5)
     align_bfm.add(button_restart_network)
     vbox = gtk.VBox()
     vbox.set_border_width(10)
     vbox.pack_start(align_bfm, False)
     return Setting(vbox, _('Restart network'), ['network'])

def show_cached_memory_amount(label):
    try:
        f = open('/proc/meminfo')
        for line in f:
            if not line.startswith('Cached:'): continue
            List = line.split()
            f.close()
            value = int(List[1])
            break
        
        label.set_text( _('No more than %s KB of memory can be reclaimed.') % value )
    except:
        import traceback
        traceback.print_exc()
    
    return True

def get_free_memory():
    f = open('/proc/meminfo')
    for line in f:
        if not line.startswith('MemFree:'): continue
        List = line.split()
        f.close()
        return int(List[1])

def free_memory(*w):
    dest = '/proc/sys/vm/drop_caches'
    import os, tempfile
    if os.path.exists(dest):
        before = get_free_memory()
        
        src = tempfile.NamedTemporaryFile('w')
        src.write('3\n')
        src.flush()
        gksudo('cp %s %s'%(src.name, dest) )

        after = get_free_memory()
        
        amount = max(0, after - before)
        
        notify( _('%s KB memory was reclaimed.')%amount, ' ')

def __reclaim_memory():
    vbox = gtk.VBox(False, 0)
    vbox.set_border_width(10)

    button_free_memory = gtk.Button( _('Reclaim memory').center(30) )
    button_free_memory.set_tooltip_text(
        _('Reclaim memory which stores pagecache, dentries and inodes.\nThis operation is done by "echo 3 >/proc/sys/vm/drop_caches"') )
    button_free_memory.connect('clicked', free_memory)
    
    label_info = gtk.Label()
    import gobject
    gobject.timeout_add(5000, show_cached_memory_amount, label_info)
    
    box = gtk.HBox(False, 10)
    box.pack_start(button_free_memory, False)
    box.pack_start(label_info, False)
    
    vbox.pack_start(box, False, False)
    return Setting(vbox, _('Reclaim memory'), ['memory'])

def get():
    return [
        __change_kernel_swappiness(),
        __reclaim_memory(),
        __restart_network() ]