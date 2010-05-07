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

class OpenJDK6(I):
    'OpenJDK 6'
    category = 'dev'
    license = GPL
    def install(self):
        APT.install('openjdk-6-jdk')
        
        env = ETCEnvironment()
        env.remove('JAVA_HOME')
        env.remove('JAVA_BIN')
        env.remove('CLASSPATH')
        env.add('JAVA_HOME', '/usr/lib/jvm/java-6-openjdk')
        env.add('JAVA_BIN', '/usr/lib/jvm/java-6-openjdk/bin')
        env.add('CLASSPATH', '.', '/usr/lib/jvm/java-6-openjdk/lib/dt.jar', '/usr/lib/jvm/java-6-openjdk/lib/tools.jar')
        env.save()
        
        run_as_root('update-java-alternatives -s java-6-openjdk', ignore_error=True)
        
        with TempOwn('/etc/jvm') as o:
            with open('/etc/jvm', "w") as f:
                f.write('/usr/lib/jvm/java-6-openjdk\n')
    def installed(self):
        return APT.installed('openjdk-6-jdk')
    def remove(self):
        APT.remove('openjdk-6-jre-lib')

        env = ETCEnvironment()
        env.remove('JAVA_HOME')
        env.remove('JAVA_BIN')
        env.remove('CLASSPATH')
        env.save()
