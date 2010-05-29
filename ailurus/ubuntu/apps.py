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
from app_tasksel import *
from app_from_external_repos import *

class OpenJDK6(I):
    'OpenJDK 6'
    category = 'saber'
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

class WorldofPadman(I):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.\n'
               'Download from ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/')
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'game'
    def install(self):
        file1 = R('ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/worldofpadman.run').download()
        run_as_root('bash ' + file1)
        file2 = R('ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/wop_patch_1_2.run').download()
        run_as_root('bash ' + file2)
        
    def installed(self):
        import os
        return os.path.exists('/usr/local/games/WoP')
        
    def remove(self):
        run_as_root('rm /usr/local/games/WoP -rf')
        run_as_root('rm /usr/local/bin/wop')

class PBC(I):
    __doc__ = _('PBC (Pairing-Based Cryptography) library')
    detail = ( _('Install Pairing-Based Cryptography library, powered by Stanford University.\n') +
               _('Official site: <span color="blue"><u>http://crypto.stanford.edu/pbc/</u></span> .') )
    category = 'library'
    license = GPL
    def install(self):
        if is32():
            fdev=R(
['http://voltar.org/pbcfiles/libpbc-dev_0.5.4-1_i386.deb'],
182700, 'f2493c4c8ad0515babf28b1c5241583d993ad169'
).download()
        else:
            fdev=R(
['http://voltar.org/pbcfiles/libpbc-dev_0.5.4-1_amd64.deb'],
206752, '6ebfb58ddb53f8c63c475f871f843e2e5c2ec676'
).download()

        if is32():
            f=R(
['http://voltar.org/pbcfiles/libpbc0_0.5.4-1_i386.deb'],
87122, '4424b14adee23683eff979c4efe33f493f2d2a55'
).download()
        else:
            f=R(
['http://voltar.org/pbcfiles/libpbc0_0.5.4-1_amd64.deb'],
96028, 'db19a612666605a18db319976b92c492e5371b91'
).download()

        APT.install_local(f, fdev)
        
    def installed(self):
        return APT.installed('libpbc0') and APT.installed('libpbc-dev')
    
    def remove(self):
        APT.remove('libpbc0', 'libpbc-dev')
    
class GNOMEArtNextGen(I):
    __doc__ = _('GNOMEArtNG: Choose 100+ GNOME themes')
    detail = _('It is able to customize the backgrounds, application look, window borders, icons, GNOME splash and GDM window. '
       'More than 100 themes can be installed, which are downloaded from http://art.gnome.org . '
       'The official site of GNOMEArtNG is http://developer.berlios.de/projects/gnomeartng/')
    category = 'theme'
    license = GPL
    DE = 'gnome'
    def install(self):
        if VERSION == 'hardy':

            file = R(
['http://download.berlios.de/gnomeartng/gnomeartng-0.7.0-hardy.deb'],
471212, '52c556fafa9664284dcff9851528f3e5aae00ebe').download()
        
        elif VERSION == 'intrepid':
        
            file = R(
['http://download.berlios.de/gnomeartng/gnomeartng-0.7.0-intrepid.deb'],
444822, '4dc42fd446ebd8e615cf6490d6ecc94a403719b8').download()
        
        elif VERSION == 'jaunty':
        
            file = R(
['http://download.berlios.de/gnomeartng/gnomeartng-0.7.0-jaunty.deb'],
441222, 'c9134ad3405c660e6e07333994ca38d494f0f90f').download()
        
        elif VERSION == 'karmic':
        
            file = R(
['http://ailurus.googlecode.com/files/gnomeartng-0.7.0-karmic.deb',],
441558, 'b2b834b1bfc76f01dce370b60ea706f6ed35e4da').download()

        else:
            raise Exception('GNOMEArtNextGen', VERSION)

        APT.install_local(file)
        
        try: # Do not raise error, when this file cannot be downloaded.
            thumb = R(['http://download.berlios.de/gnomeartng/thumbs.tar.gz'],
               15575567, '7b7dcc3709d23383c1433f90abea5bea583202f9').download()
        except:
            return
        import os
        path = os.path.expanduser('~/.gnome2/gnome-art-ng/')
        if not os.path.exists(path): run('mkdir '+path)
        with Chdir(path) as o:
            run('tar xf '+thumb)
    def installed(self):
        return APT.installed('gnomeartng')
    def remove(self):
        APT.remove('gnomeartng')
    def visible(self):
        return VERSION in ['hardy', 'intrepid', 'jaunty', 'karmic']

class DisableGetty(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def visible(self):
        return VERSION in ['hardy', 'intrepid', 'jaunty'] and os.path.exists('/etc/event.d/')
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
        return VERSION not in ['hardy', 'intrepid', 'jaunty']
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
    
class EsetNod32(I):
    __doc__ = ('Eset Nod32: a Antivirus software for Desktop Linux distributions')
    detail = _('officical site:') + 'http://beta.eset.com/linux'
    
    def install(self):
        if is32():
            f =  R(['http://download.eset.com/special/eav_linux/ueav.i386.linux'], 28642812, '9090031fc8b7dae1a12a798aa383b0513cc8100a').download()
        else:
            f = R(['http://download.eset.com/special/eav_linux/ueav.x86_64.linux'], 28828744, '9d76959c7de46bb847272af65760173ae437106a').download()
        run_as_root('chmod +x %s'%f)
        run_as_root_in_terminal(f)
    def installed(self):
        import os
        return os.path.exists('/opt/eset/')
    def remove(self):
        run_as_root('/opt/eset/esets/bin/esets_gil')
    