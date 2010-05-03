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

import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)

def method1(cache):
    for p in cache:
        if p.isInstalled and not p._depcache.IsAutoInstalled(p._pkg): print 'i',
        else: print 'u',
        print p.name

def method2(cache):
    for p in cache:
        if p.isInstalled and not p._pcache._depcache.IsAutoInstalled(p._pkg): print 'i',
        else: print 'u',
        print p.name

import apt
cache = apt.cache.Cache()
p = cache['python']
if hasattr(p, '_depcache'):
    method1(cache)
else:
    method2(cache)
