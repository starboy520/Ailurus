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
from applib import *

class _rpm_install:
    def __init__(self):
        raise Exception
    def _check(self):
        assert isinstance(self.pkgs, str)
    def install(self):
        self._check()
        RPM.install(self.pkgs)
    def installed(self):
        self._check()
        for p in self.pkgs.split():
            if not RPM.installed(p): return False
        return True
    def remove(self):
        self._check()
        RPM.remove(self.pkgs)
    def _get_reason(self, f):
        self._check()
        #evaluate
        not_in = []
        for pkg in self.pkgs.split():
            if not RPM.installed ( pkg ):
                not_in.append(pkg)
        #output
        print >>f, _('The packages "%s" are not installed.')%' '.join(not_in),

class WINE(_rpm_install):
    __doc__ = _('WINE')
    detail = _('This is an indispensable application for running Windows applications on Linux.\n'
       'Command: yum install wine')
    logo = 'wine.png'
    category = 'vm'
    def __init__(self):
        self.pkgs = 'wine'

class GEdit_Suitable_For_Programmer(_set_gconf, _rpm_install) :
    __doc__ = _('Make GEdit more suitable for programmers')
    detail = _('Change GEdit settings as follows. '
       'Automatically indent current line. '
       'Comment/uncomment codes by Ctrl+M and Shift+Ctrl+M. '
       'Indent/unindent codes by Ctrl+T and Shift+Ctrl+T. '
       'Add spell check function in "Tools" menu. '
       'Do not automatically create a hidden copy of current file. '
       'Automatically save files once in each minute. '
       'Show line numbers. \n'
       'The trick behind is to change GConf values.\n'
       '/apps/gedit-2/preferences/editor/save/auto_save = true\n'
       '/apps/gedit-2/preferences/editor/save/auto_save_interval = 1\n'
       '/apps/gedit-2/preferences/editor/save/create_backup_copy = false\n'
       '/apps/gedit-2/preferences/editor/line_numbers/display_line_numbers = true\n'
       '/apps/gedit-2/preferences/editor/auto_indent/auto_indent = true\n'
       '/apps/gedit-2/plugins/active-plugins += ["indent","codecomment","spell"]\n'
       'Then run this command: yum install gedit-plugins')
    logo = 'gedit.png'
    category = 'dev'
    def __init__(self):
        self.set = (
('/apps/gedit-2/preferences/editor/save/auto_save',True,False),
('/apps/gedit-2/preferences/editor/save/auto_save_interval',1,10),
('/apps/gedit-2/preferences/editor/save/create_backup_copy',False,True),
('/apps/gedit-2/preferences/editor/line_numbers/display_line_numbers',True,False),
('/apps/gedit-2/preferences/editor/auto_indent/auto_indent',True,False),
                    )
        self.add = (
('/apps/gedit-2/plugins/active-plugins', ['indent','codecomment','spell'] ),
                    )
        self.pkgs = 'gedit-plugins'
    def install(self):
        _set_gconf.install(self)
        _rpm_install.install(self)
    def installed(self):
        return _set_gconf.installed(self) and _rpm_install.installed(self)
    def remove(self):
        _set_gconf.remove(self)
        _rpm_install.remove(self)

class Enhance_Decompression_Capability(_rpm_install) :
    __doc__ = _('Compression/decompression support for "*.7z" and "*.cab" files')
    detail = _('Command: yum install p7zip cabextract')
    logo = 'extract.png'
    def __init__(self):
        self.pkgs = "p7zip cabextract"

class Evince_Read_Chinese_PDF(_rpm_install) :
    __doc__ = _('Make Evince be able to reveal Chinese pdf')
    detail = _('Command: yum install poppler-data')
    category='office'
    Chinese = True
    logo = 'evince.png'
    def __init__(self):
        self.pkgs = 'poppler-data'

class CHMSee_Read_CHM_Documents(_rpm_install) :
    __doc__ = _('ChmSee: A CHM file viewer')
    detail = _('Command: yum install chmsee')
    category = 'office'
    logo = 'chmsee.png'
    def __init__(self):
        self.pkgs = 'chmsee'

class Workrave_And_Auto_Start_It(_rpm_install) :
    __doc__ = 'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.\n'
       'Command: yum install workrave')
    logo = 'workrave.png'
    def __init__(self):
        self.pkgs = 'workrave'
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
    def get_reason(self, f):
        import os
        if not RPM.installed('workrave'):
            print >>f, _('"%s" is not installed.')%'workrave'
        if not os.path.exists(self.file):
            print >>f, _('The file "%s" does not exist.')%self.file,
    def remove(self):
        _rpm_install.remove(self)
        import os
        if os.path.exists(self.file):
            os.remove(self.file)

class VIM_and_VIMRC(_rpm_install) :
    __doc__ = _('VIM')
    detail = _('Install VIM and make it more suitable for programming. '
       'The installation process is as follows. '
       '"yum install vim-enhanced" command is executed. '
       'Then these lines are appended into "$HOME/.vimrc" file: \n'
       '    syntax on\n    set autoindent\n    set number\n    set mouse=a')
    category = 'dev'
    logo = 'vim.png'
    def __vimrc_installed(self):
        return file_contain ( self.vimrc, *self.lines )
    def __vimrc_install(self):
        file_append ( self.vimrc, *self.lines )
    def __init__(self):
        self.pkgs = 'vim-enhanced'
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

class ColorfulBashPromptSymbols :
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = _('Change Bash prompt symbols from '
       '"[username@hostname ~]$ " to '
       '"<span color="#3dba34">username@hostname</span> '
       '<span color="#729fcf">~</span>$ ".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       r"PS1='\[\033[01;32m\]\u@\h\[\033[00m\] \[\033[01;34m\]\W\[\033[00m\]\\$ '")
    logo = 'terminal.png'
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
    detail = _('Command: yum install cups-pdf')
    category = 'office'
    logo = 'cups.png'
    def __init__(self):
        self.pkgs = 'cups-pdf'

class Stardict_without_Dictionaries(_rpm_install):
    __doc__ = _('Stardict')
    category = 'office'
    detail = _('Command: yum install stardict\n'
               'Moreover, you can install these dictionaries by yum.\n'
               'stardict-dic-cs_CZ: Czech dictionaries\n'
               'stardict-dic-en: English dictionaries\n'
               'stardict-dic-hi: Hindi dictionary\n'
               'stardict-dic-ja: Japanese dictionaries\n'
               'stardict-dic-ru: Russian dictionaries\n'
               'stardict-dic-zh_CN: Simplified Chinese dictionaries\n'
               'stardict-dic-zh_TW: Traditional Chinese dictionaries')
    logo = 'stardict.png'
    def __init__(self):
        self.pkgs = 'stardict'

class Liferea(_rpm_install):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.\n'
       'Command: yum install liferea')
    category = 'internet'
    logo = 'liferea.png'
    def __init__(self):
        self.pkgs = 'liferea'

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
       'git: a distributed version control system.\n'
       '</i>'
       'Command: yum install '
       'gcc gcc-c++ ctags gmp-devel ncurses-devel '
       'qt3-devel subversion git')
    category = 'dev'
    logo = 'program-tools.png'
    def __init__(self):
        self.pkgs = ('gcc gcc-c++ ctags gmp-devel ncurses-devel '
                     'qt3-devel subversion git')
    def get_reason(self, f):
        self._get_reason(f)

class QtiPlot(_rpm_install) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.\n'
       'Command: yum install qtiplot')
    category = 'math'
    logo = 'qtiplot.png'
    def __init__(self):
        self.pkgs = 'qtiplot'

class QCad (_rpm_install):
    'QCad'
    detail = _('A CAD software which supports DXF-format. ')
    category = 'em'
    logo = 'qcad.png'
    def __init__(self):
        self.pkgs = 'qcad'

class DisableGetty:
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    logo = 'tty.png'
    def installed(self):
        FileServer.chdir('/etc/event.d/')
        try:
            for i in range(2,7):
                with open('tty%s'%i) as f:
                    content = f.read()
                if 'exec /sbin/' in content: return False
            return True
        finally:
            FileServer.chdir_back()
    def install(self):
        FileServer.chdir('/etc/event.d/')
        try:
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
        finally:
            FileServer.chdir_back()
    def remove(self):
        FileServer.chdir('/etc/event.d/')
        try:
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
        finally:
            FileServer.chdir_back()

class Octave(_rpm_install):
    __doc__ = 'Octave'
    detail = _(u'A Matlab® compatible numerical computation appliation.\n'
       'Command: yum install qtoctave')
    logo = 'octave.png'
    category = 'math'
    def __init__(self):
        self.pkgs = 'qtoctave'

class Generic_Genome_Browser:
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>') 
    category='biology'
    logo = 'generic_genome_browser.png'
    def install(self):
        for package in ['perl-libwww-perl', 'perl-CPAN']:
            if not RPM.installed(package):
                RPM.install(package)
        
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        su('perl ' + f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError

class TuxPaint(_rpm_install):
    'Tux Paint'
    detail = _('This is a drawing program for young children three years and up.\n' 
                    'Command: yum install tuxpaint')
    category = 'education'
    logo = 'tuxpaint.png'
    def __init__(self):
        self.pkgs='tuxpaint'

class ChildsPlay(_rpm_install):
    'ChildsPlay'
    detail = _('This is a suite of educational games for young children.\n'
                    'Command: yum install childsplay')
    category = 'education'
    logo = 'childsplay.png'
    def __init__(self):
        self.pkgs ='childsplay'
        
class GCompris(_rpm_install):
    'GCompris'
    detail = _('GCompris provides educational games for children aged 2 to 10.\n'
                    'Command: yum install gcompris')
    category = 'education'
    logo = 'gcompris.png'
    def __init__(self):
        self.pkgs = 'gcompris'

class QT_Creator(_rpm_install):
    'Qt Creator'
    detail = _('This is an IDE for Qt.\n'
               'Command: yum install qt-creator')
    category = 'dev'
    logo = 'qtcreator.png'
    def __init__(self):
        self.pkgs = 'qt-creator'

class Kadu(_rpm_install):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.\n'
               'Command : yum install kadu')
    category = 'internet'
    def __init__(self):
        self.pkgs = 'kadu'
    def support(self):
        return Config.get_show_Polish_applications()

class Parcellite(_rpm_install):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    logo = 'parcellite.png'
    def __init__(self):
        self.pkgs = 'parcellite'

class Enable_Sudo:
    __doc__ = _('Enable "sudo"')
    detail = _('If you enabled "sudo" and you want to execute commands as root, '
               'you can type command "sudo COMMAND" instead of complicated command "su -c \'COMMAND\'". '
               '<span color="red">Due to restriction on filesystem permission, '
               'Ailurus cannot detect whether "sudo" is enabled.</span> ')
    def installed(self):
        return False
    def install(self):
        su('python ../data/files/enable_sudo.py')
    def remove(self):
        pass

class Disable_Sudo:
    __doc__ = _('Disable "sudo". Prevent yourself from using "sudo".')
    def installed(self):
        return False
    def install(self):
        su('python ../data/files/disable_sudo.py')
    def remove(self):
        pass

class Disable_SELinux:
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
        su('/usr/sbin/setenforce 0')
        for path in ['/etc/sysconfig/selinux', '/etc/selinux/config']:
            with TempOwn(path) as o:
                with open(path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'SELINUX=enforcing' in line: lines[i] = 'SELINUX=permissive\n'
                with open(path, 'w') as f:
                    f.writelines(lines)
    def remove(self):
        su('/usr/sbin/setenforce 0')
        for path in ['/etc/sysconfig/selinux', '/etc/selinux/config']:
            with TempOwn(path) as o:
                with open(path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'SELINUX=permissive' in line: lines[i] = 'SELINUX=enforcing\n'
                with open(path, 'w') as f:
                    f.writelines(lines)
        su('/usr/sbin/setenforce 1')

class Wallpaper_Tray(_rpm_install):
    __doc__ = _('WallpaperTray: Randomly change GNOME desktop background')
    category = 'appearance'
    detail = _('Command: yum install wp_tray\n'
               'After installation, please restart your computer. '
               'Then right-click GNOME panel, and select "Add to panel"->"Wallpaper Tray".')
    logo = 'wallpaper-tray.png'
    def __init__(self):
        self.pkgs = 'wp_tray'
