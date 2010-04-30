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
from lib import *

def main():
    import common as COMMON
    
    DESKTOP = None
    
    if MINT or UBUNTU:
        import ubuntu as DISTRIBUTION
    elif FEDORA:
        import fedora as DISTRIBUTION
    else:
        DISTRIBUTION = None
    
    from loader import load_tips
    tips = load_tips(COMMON, DESKTOP, DISTRIBUTION)
    
    import random
    index = random.randint(0, len(tips)-1)
    tip = tips[index]
    
    notify( _('Tip of the day'), tip )

if __name__ == '__main__':
    main()