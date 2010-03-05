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

import sys
import apt

package_names = set()

for i in range(1, len(sys.argv)):
    package_names.add(sys.argv[i])
    
cache = apt.cache.Cache()
for name in package_names:
    assert name in cache

def get_manually_installed(cache):
    ret = set()
    
    def method1(cache):
        for p in cache:
            if p.isInstalled and not p._depcache.IsAutoInstalled(p._pkg): 
                ret.add(p.name)
    
    def method2(cache):
        for p in cache:
            if p.isInstalled and not p._pcache._depcache.IsAutoInstalled(p._pkg):
                ret.add(p.name)

    p = cache['python']
    if hasattr(p, '_depcache'): method1(cache)
    else:                       method2(cache)
    
    return ret

manually_installed = get_manually_installed(cache)

class Refuse(Exception): 
    pass

for name in package_names:
    cache.clear()
    p = cache[name]
    p.markDelete()
    try:
        for p in cache:
            if p.markedDelete and p.name not in package_names and p.name in manually_installed:
                raise Refuse
        print name
    except Refuse:
        pass
