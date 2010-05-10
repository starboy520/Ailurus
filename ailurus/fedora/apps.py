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

class WINE(_rpm_install):
    __doc__ = _('WINE')
    detail = _('This is an indispensable application for running Windows applications on Linux.')
    license = LGPL + ' http://wiki.winehq.org/Licensing'
    category = 'vm'
    pkgs = 'wine'
        
class Enhance_Decompression_Capability(_rpm_install) :
    __doc__ = _('Compression/decompression support for "*.7z" and "*.cab" files')
    pkgs = "p7zip cabextract"

class Evince_Read_Chinese_PDF(_rpm_install) :
    __doc__ = _('Make Evince be able to reveal Chinese, Japanese, Korean pdf')
    category='office'
    pkgs = 'poppler-data'

class CHMSee_Read_CHM_Documents(_rpm_install) :
    __doc__ = _('ChmSee: A CHM file viewer')
    category = 'office'
    license = GPL + ' http://code.google.com/p/chmsee/'
    pkgs = 'chmsee'

class Workrave_And_Auto_Start_It(_rpm_install) :
    __doc__ = 'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.')
    license = GPL + ' http://sourceforge.net/projects/workrave/'
    pkgs = 'workrave'
    def __init__(self):
        import os
        self.path = os.path.expanduser('~/.config/autostart/')
        self.file = self.path + 'workrave.desktop'
    def __workraveautostart(self):
        if not os.path.exists(self.path):
            run('mkdir -p '+self.path)
        with open(self.file, 'w') as f:
            f.write(
'''[Desktop Entry]
Name=Workrave
Exec=workrave
Encoding=UTF-8
Version=1.0
Type=Application
X-GNOME-Autostart-enabled=true
'''
            )
    def install(self):
        _rpm_install.install(self)
        self.__workraveautostart()
    def installed(self):
        import os
        if not os.path.exists(self.file): return False
        return _rpm_install.installed(self)
    def remove(self):
        _rpm_install.remove(self)
        import os
        if os.path.exists(self.file):
            os.remove(self.file)

class VIM_and_VIMRC(_rpm_install) :
    __doc__ = _('Make VIM more suitable for programming')
    detail = _('Install VIM and make it more suitable for programming. '
       'The installation process is as follows. '
       '"yum install vim-enhanced" command is executed. '
       'Then these lines are appended into "$HOME/.vimrc" file: \n'
       '    syntax on\n    set autoindent\n    set number\n    set mouse=a')
    license = GPL
    category = 'dev'
    pkgs = 'vim-enhanced'
    def __vimrc_installed(self):
        return file_contain ( self.vimrc, *self.lines )
    def __vimrc_install(self):
        file_append ( self.vimrc, *self.lines )
    def __init__(self):
        import os
        self.vimrc = os.path.expanduser("~/.vimrc")
        self.lines = [ 'syntax on', 'set autoindent', 'set number', 'set mouse=a' ]
    def install(self):
        _rpm_install.install(self)
        self.__vimrc_install()
    def installed(self):
        return _rpm_install.installed(self)
    def remove(self):
        _rpm_install.remove(self)
        file_remove ( self.vimrc, *self.lines )

class ColorfulBashPromptSymbols(I):
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = _('Change Bash prompt symbols from '
       '"[username@hostname ~]$ " to '
       '"<span color="#3dba34">username@hostname</span> '
       '<span color="#729fcf">~</span>$ ".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       r"PS1='\[\033[01;32m\]\u@\h\[\033[00m\] \[\033[01;34m\]\W\[\033[00m\]\\$ '")
    def __init__(self):
        import os
        self.__class__.detail = os.path.expandvars( self.__class__.detail )
        self.line = r"PS1='\[\033[01;32m\]\u@\h\[\033[00m\] \[\033[01;34m\]\W\[\033[00m\]\\$ '"
        self.bashrc = os.path.expandvars('$HOME/.bashrc')
    def install(self):
        file_append ( self.bashrc, self.line )
        notify( _('The color of bash prompt symbols is changed.'), _('It will take effect at the next time you log in.') )
    def installed(self):
        return file_contain ( self.bashrc, self.line )
    def remove(self):
        file_remove ( self.bashrc, self.line )

class CUPS (_rpm_install):
    __doc__ = _('Enable "Print to pdf" capability.')
    category = 'office'
    pkgs = 'cups-pdf'

class Stardict_without_Dictionaries(_rpm_install):
    __doc__ = _('Stardict')
    category = 'office'
    detail = _('You can install these dictionaries by yum.\n'
               'stardict-dic-cs_CZ: Czech dictionaries\n'
               'stardict-dic-en: English dictionaries\n'
               'stardict-dic-hi: Hindi dictionary\n'
               'stardict-dic-ja: Japanese dictionaries\n'
               'stardict-dic-ru: Russian dictionaries\n'
               'stardict-dic-zh_CN: Simplified Chinese dictionaries\n'
               'stardict-dic-zh_TW: Traditional Chinese dictionaries')
    license = GPL
    pkgs = 'stardict'

class Liferea(_rpm_install):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.')
    license = GPL
    category = 'internet'
    pkgs = 'liferea'

class CommonUsedProgrammingPackages(_rpm_install):
    __doc__ = _('Useful applications for programming')
    detail = _('The tools are:\n'
       '<i>'
       'gcc: GNU C compiler.\n'
       'gcc-c++: GNU C++ compiler.\n'
       'ctags: source code parser used in vi and emacs, which allow moving to the definition of a symbol.\n'
       'gmp-devel: GNU multiprecision arithmetic library.\n'
       'ncurses-devel: a library controlling writing to the console screen.\n'
       'qt3-devel: Trolltech Qt library, version 3.\n'
       'subversion: a version control system.\n'
       'git: a distributed version control system.'
       '</i>')
    category = 'dev'
    pkgs = ('gcc gcc-c++ ctags gmp-devel ncurses-devel '
            'qt3-devel subversion git')

class QtiPlot(_rpm_install) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.')
    category = 'math'
    license = GPL
    pkgs = 'qtiplot'

class QCad(_rpm_install):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    license = GPL
    category = 'em'
    pkgs = 'qcad'

class Alacarte(_rpm_install):
    __doc__ = ("Alacarte: menu editor")
    license = LGPL
    pkgs = 'alacarte'
    
class DisableGetty(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def installed(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                with open('tty%s'%i) as f:
                    content = f.read()
                if 'exec /sbin/' in content: return False
            return True
    def install(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                filename = 'tty%s'%i
                with open(filename) as f:
                    contents = f.readlines()
                for j, line in enumerate(contents):
                    if line.startswith('exec /sbin/'):
                        contents[j] = '#' + line[1:]
                with TempOwn(filename) as o:
                    with open(filename, 'w') as f:
                        f.writelines(contents)
    def remove(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                filename = 'tty%s'%i
                with open(filename) as f:
                    contents = f.readlines()
                for j, line in enumerate(contents):
                    if line.startswith('#xec /sbin/'):
                        contents[j] = 'e' + line[1:]
                with TempOwn(filename) as o:
                    with open(filename, 'w') as f:
                        f.writelines(contents)

class Octave(_rpm_install):
    __doc__ = _(u'Octave: A Matlab® compatible numerical computation appliation')
    license = GPL + ' http://www.gnu.org/software/octave/license.html'
    category = 'math'
    pkgs = 'qtoctave'

class Generic_Genome_Browser(I):
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>')
    license = AL
    category='biology'
    def install(self):
        for package in ['perl-libwww-perl', 'perl-CPAN']:
            if not RPM.installed(package):
                RPM.install(package)
        
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        run_as_root_in_terminal('perl ' + f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError

class TuxPaint(_rpm_install):
    __doc__ = _('Tux Paint: A drawing program for young children three years and up')
    category = 'education'
    license = GPL
    pkgs = 'tuxpaint'

class ChildsPlay(_rpm_install):
    __doc__ = _('ChildsPlay: A suite of educational games for children')
    category = 'education'
    license = GPL
    pkgs = 'childsplay'
        
class GCompris(_rpm_install):
    __doc__ = _('GCompris: Educational games for children aged 2 to 10')
    category = 'education'
    license = GPL
    pkgs = 'gcompris'

class QT_Creator(_rpm_install):
    'Qt Creator'
    detail = _('This is an IDE for Qt.')
    category = 'dev'
    license = GPL
    pkgs = 'qt-creator'

class Kadu(_rpm_install):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.\n'
               'Command : yum install kadu')
    category = 'internet'
    license = GPL
    pkgs = 'kadu'
    def support(self):
        return Config.is_Poland_locale()

class Parcellite(_rpm_install):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = GPL
    pkgs = 'parcellite'

class Enable_Sudo(I):
    __doc__ = _('Enable "sudo"')
    detail = _('If you enabled "sudo" and you want to execute commands as root, '
               'you can type command "sudo COMMAND" instead of complicated command "su -c \'COMMAND\'". '
               '<span color="red">Due to restriction on filesystem permission, '
               'Ailurus cannot detect whether "sudo" is enabled.</span> ')
    def installed(self):
        return False
    def install(self):
        run_as_root_in_terminal(D+'../support/enable_sudo')
    def remove(self):
        pass

class Disable_Sudo(I):
    __doc__ = _('Disable "sudo". Prevent yourself from using "sudo".')
    def installed(self):
        return False
    def install(self):
        run_as_root_in_terminal(D+'../support/disable_sudo')
    def remove(self):
        pass

class Disable_SELinux(I):
    __doc__ = _('Put Selinux in permissive mode, instead of enforcing mode.')
    def installed(self):
        with open('/etc/sysconfig/selinux') as f:
            c = f.read()
        if 'SELINUX=enforcing' in c: return False
        with open('/etc/selinux/config') as f:
            c = f.read()
        if 'SELINUX=enforcing' in c: return False
        return True
    def install(self):
        run_as_root_in_terminal('/usr/sbin/setenforce 0')
        for path in ['/etc/sysconfig/selinux', '/etc/selinux/config']:
            with TempOwn(path) as o:
                with open(path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'SELINUX=enforcing' in line: lines[i] = 'SELINUX=permissive\n'
                with open(path, 'w') as f:
                    f.writelines(lines)
    def remove(self):
        run_as_root_in_terminal('/usr/sbin/setenforce 0')
        for path in ['/etc/sysconfig/selinux', '/etc/selinux/config']:
            with TempOwn(path) as o:
                with open(path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'SELINUX=permissive' in line: lines[i] = 'SELINUX=enforcing\n'
                with open(path, 'w') as f:
                    f.writelines(lines)
        run_as_root_in_terminal('/usr/sbin/setenforce 1')

class Gnash(_rpm_install):
    __doc__ = _('Flash plugin for web browser')
    category = 'media'
    license = GPL
    pkgs = 'gnash gnash-plugin'
        
class Nautilus_Actions(_rpm_install):
    __doc__ = _('"Actions configuration" entry')
    detail = _('It allows the configuration of programs to be launched on files selected.\n'
               '<span color="red">This entry is not in context menu. It is in "System"->"Preferences" menu.</span>')
    license = GPL
    category = 'nautilus'
    pkgs = 'nautilus-actions'
        
class Nautilus_Image_Converter(_rpm_install):
    __doc__ = _('"Resize/Rotate images" entries')
    detail = _('Resize or rotate selected images.')
    license = GPL
    category = 'nautilus'
    pkgs = 'nautilus-image-converter'
        
class Nautilus_Open_Terminal(_rpm_install):
    __doc__ = _('"Open in terminal" entry')
    detail = _('Open a terminal in current folder.')
    license = GPL
    category = 'nautilus'
    pkgs = 'nautilus-open-terminal'
        
class Nautilus_Search_Tool(_rpm_install):
    __doc__ = _('"Search files" entries')
    license = GPL
    category = 'nautilus'
    pkgs = 'nautilus-search-tool'
    
class ImageMagick(_rpm_install):
    __doc__ = _('ImageMagick: Edit images')
    detail = _('You can start it by /usr/bin/display')
    category = 'media'
    def __init__(self):
        self.pkgs = 'ImageMagick'
        self.icon = '/usr/share/applications/imagemagick.desktop'
        
    def install(self):
        RPM.install(self.pkgs)
        path = D + 'umut_icons/imagemagick.png'
        run_as_root('cp %s /usr/share/icons/ ' % path)
        with TempOwn(self.icon) as o:
            with open(self.icon, 'w') as f:
                f.write('[Desktop Entry]\n'
    'Name=ImageMagick\n'
    'Exec=display %f\n'    
    'Encoding=UTF-8\n'
    'StartupNotify=true\n'
    'Terminal=true\n'
    'Type=Application\n'
    'Categories=GNOME;GTK;Graphics;\n'
    'Icon=/usr/share/icons/imagemagick.png\n')
        
    def remove(self):
        RPM.remove(self.pkgs)
        import os
        if os.path.exists(self.icon):
            run_as_root('rm %s' % self.icon )
        
    

class PiTiVi(_rpm_install):
    __doc__ = _('PiTiVi: Movie editor')
    license = LGPL + ' http://www.pitivi.org/'
    category = 'media'
    pkgs = 'pitivi'

class Audacity(_rpm_install):
    __doc__ = _('Audacity: Music editor')
    license = LGPL + ' http://audacity.sourceforge.net/'
    category = 'media'
    pkgs = 'audacity-freeworld'
    

class WorldofPadman(_rpm_install):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.\n'
               'Download from ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/')
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'game'
    pkgs = 'worldofpadman'

class HardwareLister(_rpm_install):
    __doc__ = _('lshw: List hardware information')
    detail = _('A small application which displays detailed hardware information')
    license = GPL
    category = 'hardware'
    pkgs = 'lshw lshw-gui'
