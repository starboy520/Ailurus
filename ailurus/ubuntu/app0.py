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

class OpenJDK6:
    'OpenJDK 6'
    category = 'dev'
    license = 'GPL'
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

class WINE_1(_apt_install):
    'WINE 1.0'
    detail = _('This is an indispensable application for running Windows applications on Linux.')
    license = ('GNU Lesser General Public License, '
               'see http://wiki.winehq.org/Licensing')
    category = 'vm'
    pkgs = 'wine wine-gecko'

class WINE_2(_apt_install):
    'WINE 1.2'
    detail = _('This is an indispensable application for running Windows applications on Linux.')
    license = ('GNU Lesser General Public License, '
               'see http://wiki.winehq.org/Licensing')
    category = 'vm'
    pkgs = 'wine1.2 wine1.2-gecko'
    def support(self):
        return APT.exist('wine1.2') and APT.exist('wine1.2-gecko')
    
# In Ubuntu Karmic, there is no need to configure WINE font substitution.
# The solution is to designate a right font.
#
#class WINE_Chinese(_apt_install):
#    __doc__ = _('WINE &amp; Wen-Quan-Yi Chinese font')
#    detail = _('WINE is an indispensable application for running Windows applications on Linux.\n'
#       'During the installation process, firstly "sudo apt-get install wine wine-gecko ttf-wqy-zenhei" command is executed, '
#       'then Wen-Quan-Yi font is used as default Chinese font.')
#    category = 'vm'
#    Chinese = True
#    pkgs = 'ttf-wqy-zenhei wine wine-gecko'
#    def __init__(self):
#        self.wqy = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
#    def install(self):
#        _apt_install.install(self)
#        import os
#        if not os.path.exists( os.path.expanduser('~/.wine') ):
#            run("wineprefixcreate") #Do not use 'winecfg' !
#        run("cp %s ~/.wine/drive_c/windows/Fonts/"%self.wqy)
#        run(r"wine regedit "+D+"../support/wine_wqy_font.reg")
#    def installed(self):
#        if not _apt_install.installed(self):
#            return False
#        import os
#        if not os.path.exists( os.path.expanduser('~/.wine') ):
#            return False
#        if not os.path.exists( os.path.expanduser('~/.wine/drive_c/windows/Fonts/wqy-zenhei.ttc') ):
#            return False
#        return True
