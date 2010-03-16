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

class GEdit_Suitable_For_Programmer(_set_gconf, _apt_install) :
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
       'Then run this command: sudo apt-get install gedit-plugins')
    size = 1828 * 1000
    time = 4
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
        _apt_install.install(self)
    def installed(self):
        return _set_gconf.installed(self) and _apt_install.installed(self)
    def remove(self):
        _set_gconf.remove(self)
        _apt_install.remove(self)

#class Full_Chinese_Language_Pack(_apt_install):
#    __doc__ = _('Install full Chinese language support')
#    detail = _('Because of live CD capacity limitation, the Ubuntu system does not have full Simplified Chinese language support.\n')
#    Chinese = True
#    size = 42156 * 1000
#    time = 38
#    logo = 'language.png'
#    def __init__(self):
#        if Config.get_Ubuntu_version()=='hardy':
#            self.pkgs='language-pack-gnome-zh-base language-pack-gnome-zh language-pack-zh-base language-pack-zh openoffice.org-l10n-zh-tw openoffice.org-help-zh-tw ttf-arphic-ukai ttf-wqy-zenhei xfonts-wqy language-support-fonts-zh libchewing3-data libchewing3 scim-chewing scim-pinyin scim-modules-table scim-tables-zh language-support-input-zh language-support-zh thunderbird-locale-zh-cn thunderbird-locale-zh-tw language-support-translations-zh openoffice.org-l10n-zh-cn openoffice.org-help-zh-cn'
#        elif Config.get_Ubuntu_version()=='intrepid':
#            self.pkgs='language-pack-gnome-zh-base language-pack-gnome-zh language-pack-zh-base language-pack-zh openoffice.org-l10n-common openoffice.org-l10n-zh-cn thunderbird-locale-zh-cn openoffice.org-l10n-zh-tw openoffice.org-help-zh-tw thunderbird-locale-zh-tw language-support-translations-zh openoffice.org-help-zh-cn ttf-arphic-ukai ttf-wqy-zenhei language-support-extra-zh xfonts-wqy language-support-fonts-zh libchewing3-data libchewing3 scim-chewing scim-pinyin scim-modules-table scim-tables-zh language-support-input-zh ttf-arphic-bsmi00lp ttf-arphic-gbsn00lp'
#        elif Config.get_Ubuntu_version()=='jaunty':
#            self.pkgs='language-pack-zh language-pack-gnome-zh language-support-input-zh language-support-fonts-zh language-support-translations-zh language-support-extra-zh'
#        elif Config.get_Ubuntu_version()=='karmic':
#            self.pkgs='language-pack-zh-hans language-pack-gnome-zh-hans openoffice.org-help-zh-cn gnome-user-guide-zh openoffice.org-l10n-zh-cn language-support-input-zh-hans language-support-fonts-zh-hans language-pack-zh-hans'
#        
#        if not getattr(self.__class__, 'appended', False) and hasattr(self, 'pkgs'):
#            self.__class__.appended = True
#            self.__class__.detail += _('Command: ')+'sudo apt-get install '+self.pkgs
#    def get_reason(self, f):
#        self._get_reason(f)

class Full_Language_Pack(_apt_install):
    __doc__ = _('Full language support and input method')
    detail = _('Because of live CD capacity limitation, the Ubuntu system does not have full language support.\n')
    logo = 'language.png'
    def __init__(self):
        import locale
        lang = locale.getdefaultlocale()
        try:
            lang = lang[0].split('_')[0]
        except AttributeError: # lang == null
            lang = 'en'

        List = [
                    'language-pack-' + lang,
                    'language-support-fonts-' + lang,
                    'language-support-input-' + lang,
                    'language-support-translations-' + lang,
                    'language-support-' + lang,
                    'language-support-writing-' + lang,
                    ]
        try:
            get_output('pgrep -u $USER gnome-panel')
            List.append('language-pack-gnome-' + lang)
        except: pass

        pkgs = []
        for p in List:
            if APT.exist(p): pkgs.append(p)

        self.pkgs = ' '.join(pkgs)

        if not getattr(self.__class__, 'appended', False) and hasattr(self, 'pkgs'):
            self.__class__.appended = True
            self.__class__.detail += _('Command: ')+'sudo apt-get install '+self.pkgs
    def get_reason(self, f):
        self._get_reason(f)

#class Eliminate_SCIM_Crash_Bug(_apt_install):
#    __doc__ = _('Eliminate bug: SCIM suddenly crashes without reason')
#    size = 172 * 1000
#    time = 3
#    logo = 'scim.png'
#    def __init__(self):
#        self.pkgs='scim-bridge-client-qt'
#    def support(self):
#        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty'] and APT.installed('scim')

class Decompression_Capability(_apt_install) :
    __doc__ = _('Decompression software: 7z, rar, cab, ace')
    detail = _('Command: sudo apt-get install rar unrar p7zip p7zip-rar p7zip-full cabextract unace')
    size = 5824 * 1000
    time = 23
    logo = 'extract.png'
    def __init__(self):
        self.pkgs = "rar unrar p7zip p7zip-rar p7zip-full cabextract unace"
    def get_reason(self, f):
        self._get_reason(f)

class Typespeed(_apt_install) :
    'Typespeed'
    detail= _('Typespeed is a typing practise. It only runs in terminal.')
    size = 356 * 1000
    category = 'game'
    logo = 'typespeed.png'
    def __init__(self):
        self.pkgs = "typespeed"

class Evince_Read_Chinese_PDF(_apt_install) :
    __doc__ = _('Make Evince be able to reveal Chinese pdf')
    detail = _('Command: sudo apt-get install poppler-data')
    category='office'
    Chinese = True
    size = 12276 * 1000
    time = 3
    logo = 'evince.png'
    def __init__(self):
        self.pkgs = 'poppler-data'

#class IA32_Libs(_apt_install) :
#    __doc__ = _('ia32 shared libraries for x86-64 systems')
#    detail = _('This is the ia32/i386 architecture runtime libraries for x86-64 Linux system.\n'
#       'Command: sudo apt-get install ia32-libs')
#    size = 125044 * 1000
#    time = 8
#    inconsistent = True
#    logo = 'ia32-libs.png'
#    def support(self):
#        return get_arch()==64
#    def __init__(self):
#        self.pkgs = 'ia32-libs'
#    def install(self):
#        if get_arch()!=32:
#            _apt_install.install(self)
#    def installed(self):
#        if get_arch()==32:
#            return True
#        return _apt_install.installed(self)
#    def remove(self):
#        if get_arch()!=32:
#            _apt_install.remove(self)

#class NTFS3G(_apt_install) :
#    __doc__ = 'NTFS-3g'
#    detail = _('This is the NTFS driver for Linux. '
#       'It supports operations on Windows XP/2000/2003/Vista/7 NTFS file system. '
#       'It supports most POSIX operations.\n'
#       'Command: sudo apt-get install ntfs-3g')
#    size = 152 * 1000
#    time = 16
#    logo = 'ntfs-3g.png'
#    def __init__(self):
#        self.pkgs = 'ntfs-3g'

class CHMSee_Read_CHM_Documents(_apt_install) :
    __doc__ = _('ChmSee: A CHM file viewer')
    detail = _('Command: sudo apt-get install chmsee')
    category = 'office'
    size = 590 * 1000
    time = 6
    logo = 'chmsee.png'
    def __init__(self):
        self.pkgs = 'chmsee'

class Workrave_And_Auto_Start_It(_apt_install) :
    __doc__ = 'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.\n'
       'Command: sudo apt-get install workrave')
    size = 1012 * 1000
    time = 5
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
        _apt_install.install(self)
        self.__workraveautostart()
    def installed(self):
        import os
        if not os.path.exists(self.file): return False
        return _apt_install.installed(self)
    def get_reason(self, f):
        import os
        if not APT.installed('workrave'):
            print >>f, _('"%s" is not installed.')%'workrave'
        if not os.path.exists(self.file):
            print >>f, _('The file "%s" does not exist.')%self.file,
    def remove(self):
        _apt_install.remove(self)
        import os
        if os.path.exists(self.file):
            os.remove(self.file)

class VIM_and_VIMRC(_apt_install) :
    __doc__ = _('VIM')
    detail = _('Install VIM and make it more suitable for programming. '
       'The installation process is as follows. '
       '"sudo apt-get install vim" command is executed. '
       'Then these lines are appended into "$HOME/.vimrc" file: \n'
       '    syntax on\n    set autoindent\n    set number\n    set mouse=a')
    category = 'dev'
    size = 1892 * 1000
    time = 4
    logo = 'vim.png'
    def __vimrc_installed(self):
        return file_contain ( self.vimrc, *self.lines )
    def __vimrc_install(self):
        file_append ( self.vimrc, *self.lines )
    def __init__(self):
        self.pkgs = 'vim'
        import os
        self.vimrc = os.path.expanduser("~/.vimrc")
        self.lines = [ 'syntax on', 'set autoindent', 'set number', 'set mouse=a' ]
    def install(self):
        _apt_install.install(self)
        self.__vimrc_install()
    def installed(self):
        return _apt_install.installed(self)
    def remove(self):
        _apt_install.remove(self)
        file_remove ( self.vimrc, *self.lines )

class ColorfulBashPromptSymbols :
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = _('Change Bash prompt symbols from '
       '"username@hostname:~$ " to '
       '"<span color="#3dba34">username@hostname</span>:'
       '<span color="#729fcf">~</span>$ ".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '")
    logo = 'terminal.png'
    def __init__(self):
        self.line = r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '"
        import os
        self.bashrc = os.path.expandvars('$HOME/.bashrc')
    def install(self):
        file_append ( self.bashrc, self.line )
        notify( _('The color of bash prompt symbols is changed.'), _('It will take effect at the next time you log in.') )
    def installed(self):
        return file_contain ( self.bashrc, self.line )
    def remove(self):
        file_remove ( self.bashrc, self.line )

class Multimedia_Codecs (_apt_install) :
    __doc__ = _('Multi-media codec')
    detail = _(
       'Command: sudo apt-get install gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad '
       'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse')
    category = 'media'
    size = 6868 * 1000
    time = 28
    logo = 'codec.png'
    def __init__(self):
        self.pkgs = ( 'gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad ' +
                      'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse' )
    def get_reason(self, f):
        self._get_reason(f)

class Eliminate_CUPS_Cannot_Print_Bug(_apt_install):
    __doc__ = _('Enable "Print to pdf" capability and eliminate "Cannot print" bug')
    detail = _('The installation process is as follows. Firstly, the command "sudo apt-get install cups-pdf" is launched. '
       'Then a bug in "/etc/apparmor.d/usr.sbin.cupsd" file is eliminated.')
    __line = '/usr/lib/cups/backend/cups-pdf flags=(complain) {\n'
    __file = '/etc/apparmor.d/usr.sbin.cupsd'
    size = 256 * 1000
    time = 4
    category = 'office'
    logo = 'cups.png'
    def __init__(self):
        self.pkgs = 'cups-pdf'
    def install(self):
        _apt_install.install(self)
        gksudo("chmod 4755 /usr/lib/cups/backend/cups-pdf") #rwsr-xr-x
        with TempOwn( self.__file ) as o:
            with open( self.__file , "r") as f:
                content = f.readlines()
                for i in range(0, len(content)):
                    if content[i].find('/usr/lib/cups/backend/cups-pdf')==0:
                        content[i]=self.__line
                        break
            with open( self.__file , "w") as f:
                for c in content:
                    f.write(c)
    def installed(self):
        return _apt_install.installed(self) and file_contain(self.__file, self.__line)

class Flash_Player(_apt_install):
    __doc__ = _(u'Adobe® Flash plugin for web browser')
    detail = _('Command: sudo apt-get install flashplugin-installer')
    time = 271
    category = 'media'
    logo = 'flash.png'
    def __init__(self):
        self.pkgs = 'flashplugin-installer'
    
class Flash_Player_Font_Bug:
    __doc__ = _('Fix font bug in Flash plugin')
    detail = _('Fix bug: characters are displayed as blank square in Flash.\n'
       'The trick behind is to modify "/etc/fonts/conf.d/49-sansserif.conf" file.')
    category = 'media'
    logo = 'flash.png'
    __file = '/etc/fonts/conf.d/49-sansserif.conf' 
    def installed(self):
        import os
        return not os.path.exists(self.__file)
    def install(self):
        try:
            FileServer.chdir('/etc/fonts/conf.d')
            import os
            if os.path.exists('49-sansserif.conf'):
                gksudo('mv 49-sansserif.conf 49-sansserif.back')
        finally:
            FileServer.chdir_back()
    def remove(self):
        try:
            FileServer.chdir('/etc/fonts/conf.d')
            import os
            if os.path.exists('49-sansserif.back'):
                gksudo('mv 49-sansserif.back 49-sansserif.conf')
        finally:
            FileServer.chdir_back()
    def get_reason(self, f):
        import os
        if os.path.exists(self.__file):
            print >>f, _('The file "%s" exists.')%self.__file

class AdobeReader:
    __doc__ = _(u'Adobe® PDF Reader')
    detail = _('Official site: http://get.adobe.com/cn/reader/')
    category = 'office'
    logo = 'adobereader.png'
    def __init__(self):
        pass
    def install(self):
        f = R(['ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.2/enu/AdbeRdr9.2-1_i386linux_enu.deb'],
                63453526, 
                'ef74e678fc072efc05d557f2b259b613530bfae4' ).download()
        DPKG.install_deb(f)
    def installed(self):
        return DPKG.installed('adobereader-enu') or APT.installed('acroread')
    def remove(self):
        if DPKG.installed('adobereader-enu'):
            gksudo('dpkg -r adobereader-enu')
        if APT.installed('acroread'):
            APT.remove('acroread')

class StardictAndDictionaries(_apt_install):
    __doc__ = _('Stardict and four dictionaries')
    category = 'office'
    detail = _('Install Stardict. '
       'Install Concise Chinese-English Dictionary, LangDao Chinese-English Dictionary, '
       'LangDao English-Chinese Dictionary and Oxford Modern English-Chinese Dictionary. '
       'Stardict official site is http://stardict.sourceforge.net/. '
       'Dictionaries are obtained from http://stardict.sourceforge.net/Dictionaries_zh_CN.php\n'
       'Command: sudo apt-get install stardict sdcv')
    time = 18
    size = 2424 * 1000 + 36796 * 1000 # deb installed size and four dictionary directories.
    Chinese = True
    logo = 'stardict.png'
    def __init__(self):
        self.pkgs = 'stardict sdcv'
        import os
        self.conf_file = os.path.expanduser('~/.stardict/stardict.cfg')
    def install(self):
        _apt_install.install(self)
        FileServer.chdir_local()
        try:
            for file in [
                R(
                  ['http://tdt.sjtu.edu.cn/S/Stardict/stardict-cedict-gb-2.4.2.tar.bz2',
                   'http://ncu.dl.sourceforge.net/project/stardict/stardict-dictionaries-zh_CN/2.4.2/stardict-cedict-gb-2.4.2.tar.bz2'],
                  726947, 
                  '7d05cd72087db22264d9c5f62f73e5e048effab0'
                  ).download(),
                R(
                  ['http://tdt.sjtu.edu.cn/S/Stardict/stardict-langdao-ce-gb-2.4.2.tar.bz2',
                   'http://ncu.dl.sourceforge.net/project/stardict/stardict-dictionaries-zh_CN/2.4.2/stardict-langdao-ce-gb-2.4.2.tar.bz2'],
                  7345014, 
                  '5a63069f17d8f1d4089cdf0662ab139089c05e61'
                  ).download(),
                R(
                  ['http://tdt.sjtu.edu.cn/S/Stardict/stardict-langdao-ec-gb-2.4.2.tar.bz2',
                   'http://ncu.dl.sourceforge.net/project/stardict/stardict-dictionaries-zh_CN/2.4.2/stardict-langdao-ec-gb-2.4.2.tar.bz2'],
                  8743872, 
                  '9c70805b8a67bbbcce0ef877f65bbc5dfcb68f68'
                  ).download(),
                R(
                  ['http://tdt.sjtu.edu.cn/S/Stardict/stardict-oxford-gb-2.4.2.tar.bz2',
                   'http://ncu.dl.sourceforge.net/project/stardict/stardict-dictionaries-zh_CN/2.4.2/stardict-oxford-gb-2.4.2.tar.bz2'],
                  7702157, 
                  '57746f37d706cc40bbd02ccdeca8e38759afd613'
                  ).download(),
                  ]:
                run("bunzip2 -f %s"%file)
                run("tar xf %s"%file[:-4])
            gksudo('rm /usr/share/stardict/dic/stardict-* -rf')
            for path in [ 'stardict-cedict-gb-2.4.2', 'stardict-langdao-ec-gb-2.4.2',
    'stardict-langdao-ce-gb-2.4.2', 'stardict-oxford-gb-2.4.2' ] :
                import os
                if not os.path.exists('/usr/share/stardict/dic/'+path):
                    gksudo("mv %s /usr/share/stardict/dic/"%path)
        finally:
            FileServer.chdir_back()

        import os
        dir_name = os.path.dirname(self.conf_file)
        if not os.path.exists(dir_name):
            run('mkdir %s'%dir_name)
        with open(self.conf_file ,'a') as f:
            f.write(r'''[/apps/stardict/preferences/dictionary]
use_custom_font=true
custom_font=FreeSerif 13''')
    def installed(self):
        if not _apt_install.installed(self):
            return False
        for path in [ 'stardict-cedict-gb-2.4.2', 'stardict-langdao-ec-gb-2.4.2',
'stardict-langdao-ce-gb-2.4.2', 'stardict-oxford-gb-2.4.2' ] :
            import os
            if not os.path.exists('/usr/share/stardict/dic/'+path): return False
        return True
    def get_reason(self, f):
        self._get_reason(f)
        #evaluate
        not_in = []
        import os
        for path in [ 'stardict-cedict-gb-2.4.2', 'stardict-langdao-ec-gb-2.4.2',
'stardict-langdao-ce-gb-2.4.2', 'stardict-oxford-gb-2.4.2' ] :
            path = '/usr/share/stardict/dic/'+path
            if not os.path.exists(path): not_in.append(path)
        #output
        if not_in:
            print >>f, _('"%s" does not exist.')%' '.join(not_in),
        
class Liferea(_apt_install):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.\n'
       'Command: sudo apt-get install liferea')
    category = 'internet'
    time = 7
    size = 3792 * 1000
    logo = 'liferea.png'
    def __init__(self):
        self.pkgs = 'liferea'

class FireWall(_apt_install):
    __doc__ = _('Firestarter')
    detail = _('Linux system comes up with a firewall "iptables". '
       'Firestarter is the graphical frontend of "iptables".\n'
       'Command: sudo apt-get install firestarter')
    category = 'internet'
    time = 9
    size = 1980 * 1000
    logo = 'firestarter.png'
    def __init__(self):
        self.pkgs = 'firestarter'

class InstallFreshLinuxKernel:
    __doc__ = _('Fresh Linux Kernel')
    detail = _(u'This is Linux kernel version 2.6.31. '
       u'It contains GEM (Graphics Execution Manager), which is the new video driver architecture of Intel®. '
       'It is downloaded from http://kernel.ubuntu.com/~kernel-ppa/mainline/')
    time = 46
    size = 163996*1000
    manual = True
    logo = 'linux-kernel.png'
    def __init__(self):
        if not hasattr(InstallFreshLinuxKernel, 'showed_current_version'):
            InstallFreshLinuxKernel.showed_current_version = True
            try:
                msg = get_output('uname -r')
                InstallFreshLinuxKernel.detail += '\n' + _('Current linux kernel version is ') + msg
            except: pass
        
        self.version = '2.6.31-02063106'
    def support(self):
        try:
            return Config.get_Ubuntu_version() in ['intrepid', 'jaunty' ]
        except:
            return False
    def install(self):
        file0 = R(
['http://tdt.sjtu.edu.cn/S/Kernel/linux-headers-2.6.31-02063106_2.6.31-02063106_all.deb',
'http://kernel.ubuntu.com/~kernel-ppa/mainline/v2.6.31.6/linux-headers-2.6.31-02063106_2.6.31-02063106_all.deb'],
9546764, 'a12429d7de28ed6cac3c25bd0d03cbc403385333').download()

        if get_arch()==32:
            file1 = R(
['http://tdt.sjtu.edu.cn/S/Kernel/linux-headers-2.6.31-02063106-generic_2.6.31-02063106_i386.deb',
'http://kernel.ubuntu.com/~kernel-ppa/mainline/v2.6.31.6/linux-headers-2.6.31-02063106-generic_2.6.31-02063106_i386.deb'],
638112, '4a7510c068e1ad094560771eb7f0b167d6e7897f').download()

            file2 = R(
['http://tdt.sjtu.edu.cn/S/Kernel/linux-image-2.6.31-02063106-generic_2.6.31-02063106_i386.deb',
'http://kernel.ubuntu.com/~kernel-ppa/mainline/v2.6.31.6/linux-image-2.6.31-02063106-generic_2.6.31-02063106_i386.deb'],
26293814, '1722fe0dcf951bcaa5e1d69fb7a18538083809a2').download()

        else:
            file1 = R(
['http://tdt.sjtu.edu.cn/S/Kernel/linux-headers-2.6.31-02063106-generic_2.6.31-02063106_amd64.deb',
'http://kernel.ubuntu.com/~kernel-ppa/mainline/v2.6.31.6/linux-headers-2.6.31-02063106-generic_2.6.31-02063106_amd64.deb'],
655102, '0b2435d40209f235d51ced231ccb9ed93488cdf9').download()

            file2 = R(
['http://tdt.sjtu.edu.cn/S/Kernel/linux-image-2.6.31-02063106-generic_2.6.31-02063106_amd64.deb',
'http://kernel.ubuntu.com/~kernel-ppa/mainline/v2.6.31.6/linux-image-2.6.31-02063106-generic_2.6.31-02063106_amd64.deb'],
25885638, '9dc9f2d740a5272450608886e9a474c01a67f98e').download()
        
        depends = []
        for file in [file0, file1, file2]:
            depends += DPKG.get_deb_depends(file)
        depends = [e for e in depends if not 'linux-headers' in e]
        APT.install(*depends)
        
        for file in [file0, file1, file2]:
            gksudo('gdebi-gtk %s'%file)
        APT.cache_changed()

    def installed(self):
        return ( APT.installed('linux-headers-%s'%self.version) and 
                 APT.installed('linux-headers-%s-generic'%self.version) and 
                 APT.installed('linux-image-%s-generic'%self.version) )
    
    def remove(self):
        APT.remove( 'linux-headers-%s'%self.version, 
                      'linux-headers-%s-generic'%self.version,
                      'linux-image-%s-generic'%self.version )
        APT.cache_changed()
