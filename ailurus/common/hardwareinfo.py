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
import traceback
import sys, os
from lib import *

def __read(path):
    with open(path) as f:
        ret = f.read().rstrip()
    return ret

def __bios():
    #The idea of this function is borrowd from cpu-g. Thanks!
    ret = []
    try:
        ret.append( row(_('BIOS vendor:'), 
             __read('/sys/devices/virtual/dmi/id/bios_vendor'), 
             D+'umut_icons/i_bios.png') )
    except:
        print >>sys.stderr, 'No such file: bios_vendor'

    try:
        ret.append( row(_('BIOS version:'), 
             __read('/sys/devices/virtual/dmi/id/bios_version'), 
             D+'umut_icons/i_bios.png') )
    except:
        print >>sys.stderr, 'No such file: bios_version'
        
    try:
        ret.append( row(_('BIOS release date:'), 
             __read('/sys/devices/virtual/dmi/id/bios_date'), 
             D+'umut_icons/i_bios.png') )
    except:
        print >>sys.stderr, 'No such file: bios_date'
    
    return ret

def __motherboard():
    ret = []
    try:
        ret.append( row(_('Motherboard name:'), 
             __read('/sys/devices/virtual/dmi/id/board_name'), 
             D+'umut_icons/i_motherboard.png') )
    except IOError: pass
    except:
        traceback.print_exc(file=sys.stderr)
        
    try:
        ret.append( row(_('Motherboard vendor:'), 
             __read('/sys/devices/virtual/dmi/id/board_vendor'), 
             D+'umut_icons/i_motherboard.png') )
    except IOError: pass
    except:
        traceback.print_exc(file=sys.stderr)
    
    return ret

def __cpu():
    ret = []
    
    try:
        core = 0
        with open('/proc/cpuinfo') as f:
            for line in f:
                v = line.split(':')
                v[0] = v[0].strip()
                if 'model name'==v[0]: core+=1
        multicore = core>1
        core = 0
        with open('/proc/cpuinfo') as f:
            for line in f:
                v = line.split(':')
                v[0] = v[0].strip()
                if v[0]=='model name':
                    core += 1
                    if multicore: string = _('CPU %s name:')%core
                    else: string = _('CPU name:')
                    ret.append( row(string, v[1].strip().replace('  ',' '), D+'umut_icons/i_cpu.png' ) )
                elif v[0]=='bogomips':
                    if multicore: string = _('CPU %s Mips:')%core
                    else: string = _('CPU Mips:')
                    ret.append( row(string, '%s'%v[1].strip(), D+'umut_icons/i_cpu.png', 
                         _('It is a measure for the computation speed. "Mips" is short for Millions of Instructions Per Second.' ) ) )
            
            _64bit = _('No')
            f.seek(0, 0)
            for line in f:
                v = line.split(':')
                v[0] = v[0].strip()
                if v[0]=='flags':
                    if ' lm ' in v[1]:
                        _64bit = _('Yes!')
            ret.append( row(_('64 bit CPU?'), _64bit, D+'umut_icons/i_cpu.png') )
    except:
        traceback.print_exc(file=sys.stderr)

    return ret

def __cpu_temp():
    try:
        import glob
        pathlist = glob.glob('/proc/acpi/thermal_zone/*')
        tempfile = None
        for path in pathlist:
            tempfile = path+'/temperature'
            import os
            if os.path.exists(tempfile):
                break
        else: 
            return []
        with open(tempfile) as f:
            for line in f:
                v = line.split(':')
            return [row(_('CPU temperature'), v[-1].strip(), D+'umut_icons/i_cpu.png')]
    except:
        traceback.print_exc(file=sys.stderr)
        return []

def __mem():
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                v = line.split(':')
                if v[0]=='MemTotal':
                    return [row(_('Total memory:'), v[1].strip(), D+'umut_icons/i_memory.png' )]
    except:
        traceback.print_exc(file=sys.stderr)
        return []

def __pci():
    ret = []
    try:
        f = get_output('lspci')
        for line in f.split('\n'):
            v = line.split(' ', 1)[1]
            v = v.split(':', 1)
            if v[0]=='Display controller':
                ret.append( row(_('Display card:'), v[1].strip(), D+'umut_icons/i_display.png' ) )
            elif v[0]=='Ethernet controller':
                ret.append( row(_('Ethernet card:'), v[1].strip(), D+'umut_icons/i_ethernet.png' ) )
            elif v[0]=='Multimedia audio controller':
                ret.append( row(_('Audio card:'), v[1].strip(), D+'umut_icons/i_audiocard.png' ) )
    except:
        traceback.print_exc(file=sys.stderr)
    return ret

def __battery():
    ret = []
    try:
        with open('/proc/acpi/battery/BAT0/state') as f:
            for line in f:
                v = line.split(':')
                if v[0] == 'charging state':
                    v = v[1].strip()
                    if v=='charged': v=_('charged')
                    elif v=='charging': v=_('charging')
                    elif v=='discharging': v=_('discharging')
                    else: raise RuntimeError(v)
                    ret.append( row(_('Battery charging state:'), v, D+'umut_icons/i_battery.png') )
                elif v[0] == 'remaining capacity':
                    ret.append( row(_('Battery remaining capacity:'), v[1].strip(), D+'umut_icons/i_battery.png') )
        
        with open('/proc/acpi/battery/BAT0/info') as f:
            for line in f:
                v = line.split(':')
                if v[0] == 'last full capacity':
                    ret.append( row(_('Battery full capacity:'), v[1].strip(), D+'umut_icons/i_battery.png') )
    except IOError: pass
    except:
        traceback.print_exc(file=sys.stderr)
    return ret

def get():
    return [ __motherboard, __bios, __cpu, __cpu_temp,
             __mem, __pci, __battery ]
