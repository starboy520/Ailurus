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
AILURUS_VERSION = '10.04.1.1'
AILURUS_RELEASE_DATE = '2010-04-02'
D = '/usr/share/ailurus/data/'
import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)

class Config:
    @classmethod
    def make_config_dir(cls):
        import os
        dir = os.path.expanduser('~/.config/ailurus/')
        if not os.path.exists(dir): # make directory
            try:    os.makedirs(dir)
            except: pass # directory exists
        if os.stat(dir).st_uid != os.getuid(): # change owner
            gksudo('chown $USER:$USER "%s"'%dir)
        if not os.access(dir, os.R_OK|os.W_OK|os.X_OK): # change access mode
            os.chmod(dir, 0755)
    @classmethod
    def get_config_dir(cls):
        import os
        return os.path.expanduser('~/.config/ailurus/')
    @classmethod
    def init(cls):
        assert not hasattr(cls, 'inited')
        cls.inited = True
        # create parser object
        import ConfigParser, os
        cls.parser = ConfigParser.RawConfigParser()
        # read configuration file if it exists
        cls.make_config_dir()
        path = cls.get_config_dir() + 'conf'
        if os.path.exists(path):
            cls.parser.read(path)
    @classmethod
    def save(cls):
        cls.make_config_dir()
        with open(cls.get_config_dir() + 'conf' , 'w') as f:
            cls.parser.write(f)
    @classmethod
    def set_string(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, (str,unicode))  and value
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_string(cls, key):
        assert isinstance(key, str) and key
        return cls.parser.get('DEFAULT', key)
    @classmethod
    def set_int(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, int)
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_int(cls, key):
        assert isinstance(key, str) and key
        value = cls.parser.get('DEFAULT', key)
        return int(value)
    @classmethod
    def set_bool(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, bool)
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_bool(cls, key):
        assert isinstance(key, str) and key
        value = cls.parser.get('DEFAULT', key)
        value = str(value)
        return value=='True' or value=='true'
    @classmethod
    def set_disable_tip(cls, value):
        cls.set_bool('disable-tip-on-startup', value)
    @classmethod
    def get_disable_tip(cls):
        try:       return cls.get_bool('disable-tip-on-startup')
        except: return False
    @classmethod
    def set_disable_clean_apt_cache(cls, value):
        cls.set_bool('disable-clean-apt-cache', value)
    @classmethod
    def get_disable_clean_apt_cache(cls):
        try: return cls.get_bool('disable-clean-apt-cache')
        except: return True
    @classmethod
    def get_locale(cls):
        import locale
        value = locale.getdefaultlocale()[0]
        if value: return value # language code and encoding may be None if their values cannot be determined.
        else: return 'en_US'
    @classmethod
    def is_Chinese_locale(cls):
        return cls.get_locale().startswith('zh')
    @classmethod
    def is_Poland_locale(cls):
        return cls.get_locale().startswith('pl')
    @classmethod
    def supported_Ubuntu_version(cls, version):
        assert isinstance(version, str) and version
        return version in ['hardy', 'intrepid', 'jaunty', 'karmic', 'lucid', ]
    @classmethod
    def is_Ubuntu(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): 
            return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'Ubuntu' in c
    @classmethod
    def set_Ubuntu_version(cls, version):
        if not cls.supported_Ubuntu_version(version):
            raise ValueError
        cls.set_string('ubuntu-version', version)
    @classmethod
    def get_Ubuntu_version(cls):
        '''return 'hardy', 'intrepid', 'jaunty', 'karmic' or 'lucid'.'''
        if cls.is_Ubuntu():
            with open('/etc/lsb-release') as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith('DISTRIB_CODENAME='):
                    return line.split('=')[1].strip()
        value = cls.get_string('ubuntu-version')
        assert cls.supported_Ubuntu_version(value), value
        return value
    @classmethod
    def is_Mint(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'LinuxMint' in c
    @classmethod
    def get_Mint_version(cls):
        '''return '5', '6', '7' or '8'. '''
        import os
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_RELEASE='):
                return line.split('=')[1].strip()
    @classmethod
    def is_Fedora(cls):
        import os
        return os.path.exists('/etc/fedora-release')
    @classmethod
    def get_Fedora_version(cls):
        with open('/etc/fedora-release') as f:
            c = f.read()
        return c.split()[2].strip()
    @classmethod
    def is_GNOME(cls):
        if cls.is_XFCE(): return False
        try:
            get_output('pgrep -u $USER gnome-panel')
            return True
        except:
            return False
    @classmethod
    def is_XFCE(cls):
        try:  
            get_output('pgrep -u $USER xfce4-session')
            return True
        except: 
            return False
    @classmethod
    def wget_set_timeout(cls, timeout):
        assert isinstance(timeout, int) and timeout>0, timeout
        cls.set_int('wget_timeout', timeout)
    @classmethod
    def wget_get_timeout(cls):
        try:       value = cls.get_int('wget_timeout')
        except: value = 20
        return value
    @classmethod
    def wget_set_triesnum(cls, triesnum):
        assert isinstance(triesnum, int) and triesnum>0, triesnum
        cls.set_int('wget_triesnum', triesnum)
    @classmethod
    def wget_get_triesnum(cls):
        try:       value = cls.get_int('wget_triesnum')
        except: value = 3
        return value
    @classmethod
    def set_fastest_repository(cls, value):
        assert ':' in value
        cls.set_string('fastest_repository', value)
    @classmethod
    def get_fastest_repository(cls):
        return cls.get_string('fastest_repository')
    @classmethod
    def set_fastest_repository_response_time(cls, value):
        cls.set_int('fastest_repository_response_time', value)
    @classmethod
    def get_fastest_repository_response_time(cls):
        return cls.get_int('fastest_repository_response_time')

Config.init()

class ShowALinuxSkill:
    @classmethod
    def installed(cls):
        import os
        path = os.path.expanduser('~/.config/autostart/show-a-linux-skill-bubble.desktop')
        return os.path.exists(path)
    @classmethod
    def install(cls):
        import os
        dir = os.path.expanduser('~/.config/autostart/')
        if not os.path.exists(dir): os.system('mkdir %s -p' % dir)
        file = dir + 'show-a-linux-skill-bubble.desktop'
        with open(file, 'w') as f:
            f.write('[Desktop Entry]\n'
                    'Name=Show a random Linux skill after logging in.\n'
                    'Comment=Show a random Linux skill after you log in to GNOME. Help you learn Linux.\n'
                    'Exec=/usr/share/ailurus/support/show-a-linux-skill-bubble\n'
                    'Terminal=false\n'
                    'Type=Application\n'
                    'Icon=/usr/share/ailurus/data/suyun_icons/shortcut.png\n'
                    'Categories=System;\n'
                    'StartupNotify=false\n')
    @classmethod
    def remove(cls):
        import os
        path = os.path.expanduser('~/.config/autostart/show-a-linux-skill-bubble.desktop')
        os.system('rm %s -f'%path)

try:
    Config.get_bool('show-a-linux-skill-bubble')
except:
    try:
        Config.set_bool('show-a-linux-skill-bubble', True)
        ShowALinuxSkill.install()
    except:
        import traceback
        traceback.print_exc()

def install_locale(force_reload=False):
    assert isinstance(force_reload, bool)
    
    if force_reload or getattr(install_locale, 'installed', False)==False:
        install_locale.installed = True
    else: return

    import gettext
    gettext.translation('ailurus', '/usr/share/locale', fallback=True).install(names=['ngettext'])

install_locale()

class CommandFailError(Exception):
    'Fail to execute a command'
    def __init__(self, *args):
        new_args = list(args)
        import os
        arch = os.uname()[-1]
        new_args.append(arch)
        try:
            with open('/etc/lsb-release') as f:
                new_args.append(f.read().strip())
        except: pass
        try:
            with open('/etc/fedora-release') as f:
                new_args.append(f.read().strip())
        except: pass
        Exception.__init__(self, *new_args)

def run(cmd, ignore_error=False):
    is_string_not_empty(cmd)
    if not isinstance(ignore_error,  bool): raise TypeError

    if getattr(run, 'terminal', None):
        assert run.terminal.__class__.__name__ == 'Terminal'
        try:
            run.terminal.run(cmd)
        except CommandFailError:
            if not ignore_error: raise
    else:
        print '\x1b[1;33m', _('Run command:'), cmd, '\x1b[m'
        import os
        if os.system(cmd) and not ignore_error: raise CommandFailError(cmd)

def pack(D):
    assert isinstance(D, dict)
    import StringIO
    buf = StringIO.StringIO()
    for k,v in D.items():
        print >>buf, k
        print >>buf, v
    return buf.getvalue()

def packed_env_string():
    import os
    env = dict( os.environ )
    env['PWD'] = os.getcwd()
    return pack(env)

def get_authentication_method():
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    ret = obj.get_check_permission_method(dbus_interface='cn.ailurus.Interface')
    ret = int(ret)
    assert ret == 0 or ret == 1, ret
    return ret

def authenticate():
    if get_authentication_method() == 0:
        import dbus
        bus = dbus.SessionBus()
        policykit = bus.get_object('org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        import os
        policykit.ObtainAuthorization('cn.ailurus', dbus.UInt32(0), dbus.UInt32(os.getpid()))

def su_spawn(command):
    is_string_not_empty(command)
    
    authenticate()
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    obj.spawn(command, packed_env_string(), dbus_interface='cn.ailurus.Interface')

def gksudo(cmd, ignore_error=False):
    is_string_not_empty(cmd)
    assert isinstance(ignore_error, bool)
    
    import os
    if os.getuid()!=0:
        print '\x1b[1;33m', _('Run command:'), cmd, '\x1b[m'
        authenticate()
        import dbus
        bus = dbus.SystemBus()
        obj = bus.get_object('cn.ailurus', '/')
        obj.run(cmd, packed_env_string(), ignore_error, timeout=36000, dbus_interface='cn.ailurus.Interface')
    else:
        run(cmd, ignore_error)

def is_string_not_empty(string):
    if type(string)!=str and type(string)!=unicode: raise TypeError(string)
    if string=='': raise ValueError

def get_output(cmd, ignore_error=False):
    is_string_not_empty(cmd)
    assert isinstance(ignore_error, bool)
    
    import commands
    status, output=commands.getstatusoutput(cmd)
    if status and not ignore_error: raise CommandFailError(cmd)
    return output
    
#def keep_sudo():
#    'run "sudo -v" one time for each minute'
#    'This function is not used.'
#    while True:
#        import time
#        time.sleep(60)
#        if os.system('sudo -v'):
#            raise CommandFailError, 'sudo -v'

class TempOwn:
    def __init__(self,path):
        is_string_not_empty(path)
        if path[0]=='-':
            raise ValueError
        import os
        if not os.path.exists(path):
            gksudo('touch "%s"'%path)
        gksudo('chown $USER:$USER %s'%path )
        self.path = path
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        gksudo('chown root:root %s'%self.path)

def notify(title, content):
    'Show a notification in the right-upper corner.'
    is_string_not_empty(title)
    is_string_not_empty(content)
    if not hasattr(notify, 'inited'):
        notify.inited = True
        import pynotify
        pynotify.init('Trusted Digital Technology Laboratory, Shanghai Jiao Tong Univ., China.')

    try:
        import pynotify, os
        icon = D+'suyun_icons/notify-icon.png'
        n=pynotify.Notification(title, content, icon)
        n.show()
    except:
        import sys, traceback
        traceback.print_exc(file=sys.stderr)
        print >>sys.stderr, content

#def is_started_by_sudo():
#    'Return True if this program is started by "sudo"'
#    'Return False if it is started by normal user or "su"'
#    import os
#    return os.getuid()==0 and os.getenv("HOME")!="/root"

def get_arch():
    'Return 64 if the operating system is 64-bit. Return 32 otherwise.'
    import os
    if os.uname()[-1] == 'x86_64': return 64
    return 32

def file_contain(path, *lines):
    'Return True if the file contains all the lines'
    is_string_not_empty(path)
    if not len(lines): raise ValueError
    for line in lines:
        is_string_not_empty(line)
    import os
    if os.path.exists(path):
        with open(path, 'r') as f:
            contents = f.readlines()
        for line in lines:
            if line[-1]!='\n': line+='\n'
            if not line in contents: return False
        return True
    return False

def file_insert(path, *args):
    'Insert lines into file. The format of args is "position, line, position, line..."'
    is_string_not_empty(path)
    if not len(args): raise ValueError
    for i in range(0, len(args), 2):
        if type(args[i])!=int: raise TypeError
        is_string_not_empty(args[i+1])
    
    import os
    if not os.path.exists(path):
        run('touch %s'%path)
    with open(path, "r") as f:
        contents = f.readlines()
    for i in range(0, len(args), 2):
        line = args[i]
        string = args[i+1]
        if string[-1]!='\n': string+='\n'
        contents.insert(line, string)
    with open(path, "w") as f:
        f.writelines(contents)

def file_append(path, *lines):
    is_string_not_empty(path)
    if not len(lines): raise ValueError
    for line in lines:
        is_string_not_empty(line)
    with open(path, 'a') as f:
        for line in lines:
            if line[-1]!='\n': line+='\n'
            f.write(line)

def file_remove(path, *lines):
    is_string_not_empty(path)
    if not len(lines): raise ValueError
    for line in lines:
        is_string_not_empty(line)
    with open(path, "r") as f:
        contents = f.readlines()
    for line in lines:
        if line[-1]!='\n': line+='\n'
        try: 
            contents.remove(line)
        except ValueError: pass
    with open(path, "w") as f:
        f.writelines(contents)

def free_space(path):
    is_string_not_empty(path)
    assert path[0]=='/'
    import os, statvfs
    e = os.statvfs(path)
    return e[statvfs.F_BAVAIL] * e[statvfs.F_BSIZE]

def own_by_user(*paths):
    if not len(paths): raise ValueError
    for path in paths:
        is_string_not_empty(path)
        if path[0]=='-': raise ValueError
    for path in paths:
        import os
        if os.stat(path).st_uid != os.getuid():
            gksudo('chown $USER:$USER "%s"'%path)

class FileServer:
    @classmethod
    def chdir(cls, path):
        is_string_not_empty(path)
        import os
        cls.__saved_path = os.getcwd()
        os.chdir(path)
    @classmethod
    def chdir_local(cls):
        import os
        cls.__saved_path = os.getcwd()
        if not os.path.exists('/var/cache/ailurus/'):
            gksudo('mkdir -p /var/cache/ailurus/')
            gksudo('chown $USER:$USER /var/cache/ailurus/')
        os.chdir('/var/cache/ailurus/')
    @classmethod
    def chdir_back(cls):
        import os
        os.chdir(cls.__saved_path)

def is_pkg_list(packages):
    if not len(packages): raise ValueError
    for package in packages:
        is_string_not_empty(package)
        if package[0]=='-': raise ValueError
        if ' ' in package: raise ValueError

def su(command):
    is_string_not_empty(command)
    print '\x1b[1;33m', _('Run command:'), command, '\x1b[m'

    import tempfile
    t = tempfile.NamedTemporaryFile('w')
    t.write(command)
    t.flush()
    string = 'LANG=C xterm -T "Ailurus Terminal" -e bash %s' % t.name

    authenticate()
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    obj.run(string, packed_env_string(), False, timeout=36000, dbus_interface='cn.ailurus.Interface')

class RPM:
    fresh_cache = False
    __set1 = set()
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if getattr(cls, 'fresh_cache', False): return
        cls.fresh_cache = True
        del cls.__set1
        cls.__set1 = set()
        import subprocess, os
        path = os.path.dirname(os.path.abspath(__file__)) + '/support/dumprpmcache.py'
        task = subprocess.Popen(['python', path],
            stdout=subprocess.PIPE,
            )
        for line in task.stdout:
            cls.__set1.add(line[:-1])
    @classmethod
    def installed(cls, package_name):
        is_pkg_list([package_name])
        cls.refresh_cache()
        return package_name in cls.__set1
    @classmethod
    def install(cls, *package):
        su('yum install %s -y' % ' '.join(package))
        cls.cache_changed()
    @classmethod
    def install_local(cls, path):
        assert isinstance(path, str)
        import os
        assert os.path.exists(path)
        
        su('yum localinstall --nogpgcheck -y %s' % path)
        cls.cache_changed()
    @classmethod
    def remove(cls, *package):
        su('yum remove %s -y' % ' '.join(package))
        cls.cache_changed()
    @classmethod
    def import_key(cls, path):
        assert isinstance(path, str)
        su('rpm --import %s' % path)

class APT:
    fresh_cache = False
    __set1 = set()
    __set2 = set()
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if getattr(cls, 'fresh_cache', False): return
        cls.fresh_cache = True
        del cls.__set1
        del cls.__set2
        cls.__set1 = set()
        cls.__set2 = set()
        import subprocess, os
        path = os.path.dirname(os.path.abspath(__file__))+'/support/dumpaptcache.py'
        task = subprocess.Popen(['python', path],
            stdout=subprocess.PIPE,
            )
        for line in task.stdout:
            name = line[2:-1]
            if line[0]=='i': cls.__set1.add(name)
            else: cls.__set2.add(name)
    @classmethod
    def get_installed_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__set1
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__set2
    @classmethod
    def installed(cls, package_name):
        is_pkg_list([package_name])
        cls.refresh_cache()
        return package_name in cls.__set1
    @classmethod
    def exist(cls, package_name):
        is_pkg_list([package_name])
        cls.refresh_cache()
        return package_name in cls.__set1 or package_name in cls.__set2
    @classmethod
    def install(cls, *packages):
        # (c) 2005-2007 Canonical, GPL
        is_pkg_list(packages)
        # get list of not-existed packages
        not_exist = [ e for e in packages if not APT.exist(e) ]
        # reduce package list
        packages = [ e for e in packages if not APT.installed(e) ]
        if packages:
            # apt-get update
            if not hasattr(cls, 'updated'):
                APT.apt_get_update()
                cls.updated = True
            # create packages-list
            import tempfile
            f = tempfile.NamedTemporaryFile()
            for item in packages:
                f.write("%s\tinstall\n" % item)
            f.flush()
            # construct command
            import os
            cmd = ["/usr/sbin/synaptic",
                    "--hide-main-window",
                    "--non-interactive",
                    "-o", "Synaptic::closeZvt=true", ]
            cmd.append("--set-selections-file")
            cmd.append("%s" % f.name)
            # print message
            print '\x1b[1;33m', _('Installing packages:'), ' '.join(packages), '\x1b[m'
            # run command
            gksudo(' '.join(cmd))
            # notify change
            APT.cache_changed()
        # check state
        failed = []
        for p in packages:
            if not APT.installed(p): failed.append(p)
        if failed or not_exist:
            msg = _('Cannot install packages "%s".')%' '.join(failed+not_exist)
            raise CommandFailError(msg)
    @classmethod
    def remove(cls, *packages):
        # (c) 2005-2007 Canonical, GPL
        is_pkg_list(packages)
        # get list of not-existed packages
        not_exist = [ e for e in packages if not APT.exist(e) ]
        # reduce package list
        packages = [ e for e in packages if APT.installed(e) ]
        if packages:
            # create packages-list
            import tempfile
            f = tempfile.NamedTemporaryFile()
            for item in packages:
                f.write("%s\tuninstall\n" % item)
            f.flush()
            # construct command
            import os
            cmd = ["/usr/sbin/synaptic",
                    "--hide-main-window",
                    "--non-interactive",
                    "-o", "Synaptic::closeZvt=true", ]
            cmd.append("--set-selections-file")
            cmd.append("%s" % f.name)
            # print message
            print '\x1b[1;31m', _('Removing packages:'), ' '.join(packages), '\x1b[m'
            # run command
            gksudo(' '.join(cmd))
            # notify change
            APT.cache_changed()
        # check state
        failed = []
        for p in packages:
            if APT.installed(p): failed.append(p)
        if failed or not_exist:
            msg = _('Cannot remove packages "%s".')%' '.join(failed+not_exist)
            raise CommandFailError(msg)
    @classmethod
    def apt_get_update(cls):
        # (c) 2005-2007 Canonical, GPL
        print '\x1b[1;33m', _('Run "apt-get update". Please wait for few minutes.'), '\x1b[m'
        cmd = "/usr/sbin/synaptic --hide-main-window --non-interactive -o Synaptic::closeZvt=true --update-at-startup"
        gksudo(cmd, ignore_error=True)

#class DPKG:
#    @classmethod
#    def installed(cls, package_name):
#        is_pkg_list([package_name])
#        seed = 'Package: %s\n'%package_name
#        with open('/var/lib/dpkg/status') as f:
#            while True:
#                line = f.readline()
#                if len(line)==0: return False
#                if line==seed:
#                    status = ''
#                    while not status.startswith('Status:'):
#                        status = f.readline()
#                    return status=='Status: install ok installed\n'
#    @classmethod
#    def exist(cls, package_name):
#        seed = 'Package: %s\n'%package_name
#        with open('/var/lib/dpkg/available') as f:
#            for line in f:
#                if line==seed:
#                    return True
#        return False

#def package_status( package_name ):
#    is_pkg_list([package_name])
#    
#    if not hasattr(package_status, 'inited'):
#        package_status.inited=True
#        import apt
#        package_status.cache=apt.cache.Cache()
#    
#    if getattr(package_status, 'cache_changed', False):
#        package_status.cache_changed=False
#        package_status.cache.open(None)
#        
#    cache = package_status.cache
#    if not package_name in cache:
#        return False
#    return cache[package_name].isInstalled

#def package_exists( package_name ):
#    is_string_not_empty(package_name)
#    if package_name[0]=='-': raise ValueError
#
#    if not hasattr(package_status, 'inited'):
#        package_status.inited=True
#        package_status.cache=apt.cache.Cache()
#    return package_name in package_status.cache

#def installed(*packages):
#    is_pkg_list(packages)
#    for pkg in packages:
#        if not package_status ( pkg ):
#            return False
#    return True

class DPKG:
    @classmethod
    def installed(cls, package_name):
        'Return True if the package is installed. False if not installed or not exist.'
        is_pkg_list([package_name])
        import commands
        status, output = commands.getstatusoutput( 'LANG=C dpkg-query -l %s'%package_name )
        if status == 0 : 
            return output.split('\n')[-1][1] == 'i'
        elif status == 256 : # package does not exist
            return False
        raise CommandFailError # other error reason
    @classmethod
    def get_deb_depends(cls, filename):
        is_pkg_list([filename])
        import os
        if os.path.splitext(filename)[1]!='.deb': raise ValueError
        if not os.path.exists(filename): raise ValueError
        output = get_output('LANG=C dpkg --info %s' % filename)
        import re
        match=re.search('Depends: (.*)', output)
        if match is None: # no depends 
            return [] 
        items=match.group(1).split( ',' )
        depends = []
        for item in items:
            depends.append( item.split()[0] )
        return depends
    @classmethod
    def install_deb(cls, *packages):
        is_pkg_list(packages)
        for package in packages:
            import os
            if os.path.splitext(package)[1]!='.deb': raise ValueError
            if not os.path.exists(package): raise ValueError
            depends = DPKG.get_deb_depends(package)
            if len(depends):
                APT.install(*depends)
            gksudo('dpkg --install --force-architecture %s'%package)
            APT.cache_changed()
    @classmethod
    def remove_deb(cls, package_name):
        is_string_not_empty(package_name)
        gksudo('dpkg -r %s'%package_name)
        APT.cache_changed()

def get_response_time(url):
    is_string_not_empty(url)

    import urllib2
    import time
    import sys
    begin = time.time()
    if sys.version_info>(2,5): # for python 2.6+
        urllib2.urlopen(url, timeout=3)
    else: # for python 2.5
        urllib2.urlopen(url) # FIXME: no timeout!
    end = time.time()
    return (end - begin) * 1000 # in milliseconds

def derive_size(size):
    if not ( isinstance(size, int) or isinstance(size, long) ): raise TypeError
    if not size>=0: raise ValueError
    _1G = 1e9
    _1M = 1e6
    _1K = 1e3
    if size>=_1G:
        return _('%.1f GB') % ( size/_1G )
    if size>=_1M:
        return _('%.1f MB') % ( size/_1M )
    if size>=_1K:
        return _('%.1f KB') % ( size/_1K )
    return _('%s bytes') % int(size)

def derive_time(time):
    if not isinstance(time, int): raise TypeError
    if not time>=0: raise ValueError
    _1h = 3600.
    _1m = 60.
    if time >= _1h:
        return _('%.1f hours') % ( time/_1h )
    if time >= _1m:
        return _('%.1f minutes') % ( time/_1m )
    return _('%d seconds') % time

#def print_progress(command, total_line_number):
#    def color_print(progress):
#        assert 0<=progress<=100
#        print '\r\x1b[1;36m'+' %.2f%%'.ljust(8) % progress+'\x1b[m',
#    assert isinstance(command, str)
#    assert total_line_number > 0
#    print '\x1b[1;33m%s\x1b[m'%command
#    linenum = 0
#    import subprocess
#    task = subprocess.Popen(command, shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
#    while True:
#        string = task.readline()
#        linenum+=1
#        if len(string)==0: # EOF
#            break
#        color_print (min(99, 100.*linenum/total_line_number))
#    color_print (100)
#    print # print a new-line at last

class KillWhenExit:
    task_list = []
    @classmethod
    def add(cls, task):
        import subprocess
        if not isinstance(task, (str, unicode, subprocess.Popen)): raise TypeError
        if isinstance(task, (str, unicode)):
            assert task!=''
            print '\x1b[1;33m', _('Run command:'), task, '\x1b[m' 
            task=subprocess.Popen(task, shell=True)
        cls.task_list.append(task)
    @classmethod
    def kill_all(cls):
        for task in cls.task_list:
            try:
                import os, signal
                os.kill(task.pid, signal.SIGTERM)
            except:
                import traceback, sys
                traceback.print_exc(file=sys.stderr)
        cls.task_list = []

import atexit
atexit.register(KillWhenExit.kill_all)

def wget(url, filename):
    is_string_not_empty(url)
    assert url[0]!='-'
    is_string_not_empty(filename)
    assert filename[0]!='-'
    try:
        timeout = Config.wget_get_timeout()
        tries = Config.wget_get_triesnum()

        run("wget --timeout=%(timeout)s --tries=%(tries)s '%(url)s' -O '%(filename)s' "
            %{'timeout':timeout, 'tries':tries, 'url':url, 'filename':filename} )
    except:
        import os
        if os.path.exists(filename): os.unlink(filename)
        raise
    
def reset_dir():
    import os, sys
    if sys.argv[0]!='':
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

class APTSource:
    @classmethod
    def apt_source_files_list(cls):
        'Return a list of apt source files'
        import glob, os
        ret = glob.glob('/etc/apt/sources.list.d/*.list')
        if os.path.exists('/etc/apt/sources.list'):
            ret.append('/etc/apt/sources.list')
        return ret
    @classmethod
    def current_servers(cls):
        'Return a list of currently used apt servers'
        ret = set()
    
        for file in APTSource.apt_source_files_list():
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    if len(line)==0 or line[0]=='#': continue # skip blank lines or comments
                    import re
                    match = re.match(r'^deb(-src)? http://([^/]+)/.*$', line)
                    if match:
                        server = match.group(2)
                        ret.add(server)
    
        ret = list(ret)
        ret.sort()
        return ret
    @classmethod
    def change_servers_in_source_files(cls, changes):
        'Input a dict: old_server->new_server'
        'Change servers in all source files'

        if not isinstance(changes, dict): raise TypeError
        for key, value in changes.items():
            is_string_not_empty(key)
            is_string_not_empty(value)
        
        for file in APTSource.apt_source_files_list():
            # read content
            with open(file) as f:
                contents = f.readlines()
                
            # do replacement
            changed = False
            for i, line in enumerate(contents):
                # skip blank lines and commented lines
                if len(line.strip())==0 or line.strip()[0]=='#': continue
                string = line.split('#')[0]
                for old, new in changes.items():
                    if old in string:
                        contents[i] = line.replace(old, new, 1)
                        changed = True
                        break
            
            # write back
            if changed:
                with TempOwn(file) as o:
                    with open(file, 'w') as f:
                        f.writelines(contents)
    @classmethod
    def get_source_contents(cls):
        'Return a dict: file_name->file_content'
        ret = {}
        for file in APTSource.apt_source_files_list():
            with open(file) as f:
                contents = f.readlines()
            ret[file] = contents
        return ret
    @classmethod
    def get_apt_source_config_content(cls, strip_comments=False):
        if not isinstance(strip_comments, bool): raise TypeError
        
        ret = []
        for file in APTSource.apt_source_files_list():
            if strip_comments:
                with open(file) as f:
                    for line in f:
                        line = line.strip()
                        if len(line)==0 or line[0]=='#': continue # skip comments and blank lines
                        line = line.split('#', 1)[0] # strip comments
                        ret.append(line+'\n')
            else:
                with open(file) as f:
                    for line in f:
                        if line[-1]!='\n': line+='\n'
                        ret.append(line)
        return ''.join(ret)

def parse_maintainer(string):
    is_string_not_empty(string)
    
    if not hasattr(parse_maintainer, 'init'):
        import re
        parse_maintainer.p1 = re.compile(r'^(.+)(?P<webpage>https?://.+)$')
        parse_maintainer.p2 = re.compile(r'^(.+)<(?P<email>.+)>$')
        parse_maintainer.init = True
    match = parse_maintainer.p1.match(string)
    name = email = webpage = None
    if match:
        webpage=match.group('webpage')
        string = match.group(1).strip()
    match = parse_maintainer.p2.match(string)
    if match:
        email = match.group('email')
        name = match.group(1).strip()
    else:
        name = string
    return name, email, webpage

import threading
class PingThread(threading.Thread):
    def __init__(self, url, server, result):
        is_string_not_empty(url)
        is_string_not_empty(server)
        assert isinstance(result, list)
        
        threading.Thread.__init__(self)
        self.url = url
        self.server = server
        self.result = result
    def run(self):
        try:
            time = get_response_time(self.url)
            self.result.append([self.server, time])
        except:
            self.result.append([self.server, 'unreachable'])

def open_web_page(page):
    is_string_not_empty(page)
    notify( _('Opening web page'), page)
    KillWhenExit.add('xdg-open %s'%page)

def report_bug(*w):
    page = 'http://code.google.com/p/ailurus/issues/entry'
    notify( _('Opening web page'), page)
    KillWhenExit.add('xdg-open %s'%page)

class FirefoxExtensions:
    @classmethod
    def get_extensions_path(cls):
        import os
        path = os.path.expandvars('$HOME/.mozilla/firefox')
        assert os.path.exists(path), path
        ini = '%s/profiles.ini'%path
        assert os.path.exists(ini), ini
        with open(ini) as f:
            default_found = False
            for line in f:
                if not default_found:
                    if line=='Name=default\n':
                        default_found = True
                    continue
                else:
                    if line.find('Path=')==0:
                        default_profile_path = line[5:-1]
                        break
            else:
                raise Exception('default profile not found')
        return '%s/%s/extensions'%(path,default_profile_path)
    
    @classmethod
    def analysis_method1(cls, doc):
        import re
        try:       return re.search('em:name="(.+)"', doc).group(1)
        except: return None
    @classmethod
    def analysis_method2(cls, doc):
        import re
        try:       return re.search('<em:name>(.+)</em:name>', doc).group(1)
        except: return None
    @classmethod
    def analysis_extension(cls, extension_path, ret):
        import os
        if os.path.isdir(extension_path)==False: return
        
        try:
            rdf = '%s/install.rdf'%extension_path
            if not os.path.exists(rdf): 
                return
            
            with open(rdf) as f:
                doc = f.read()
            name = cls.analysis_method1(doc) or cls.analysis_method2(doc)  
            if name: ret.append(name) 
        except:
            import traceback
            traceback.print_exc()
    
    @classmethod
    def __get_extensions_basic(cls):
        import os, traceback, glob
        try:
            ret = []
            extensions_path = cls.get_extensions_path()
            assert os.path.exists(extensions_path), extensions_path
            extensions = glob.glob('%s/*'%extensions_path)
            for extension in extensions:
                cls.analysis_extension(extension, ret)
            return ret
        except:
            traceback.print_exc()
            return []
    
    @classmethod
    def get_extensions(cls, force_reload = False):
        if not hasattr(cls, 'cache_get_extensions') or force_reload:
            cls.cache_get_extensions = cls.__get_extensions_basic()
        return cls.cache_get_extensions
    
    @classmethod
    def installed(cls, extension_name):
        assert isinstance(extension_name, (str, unicode))
        ret = cls.get_extensions()
        return extension_name in ret

def delay_notify_firefox_restart(show_notify=False):
    assert isinstance(show_notify, bool)
    if not show_notify:
        delay_notify_firefox_restart.should_show = True
    else:
        if getattr(delay_notify_firefox_restart, 'should_show', False):
            delay_notify_firefox_restart.should_show = False
            try:
                string = get_output('ps -a -u $USER | grep firefox', True)
                if string!='':
                    notify('Please restart Firefox', 'Please restart Firefox to complete installation.')
                else:
                    KillWhenExit.add('firefox')
            except:
                import traceback
                traceback.print_exc(file=sys.stderr)
                notify('Please restart Firefox', 'Please restart Firefox to complete installation.')

def sha1(path):
    is_string_not_empty(path)
    import os
    assert os.path.exists(path)
    import hashlib
    obj = hashlib.sha1()
    f = open(path)
    while True:
        block = f.read(4096)
        if len(block)==0: break
        obj.update(block)
    f.close()
    return obj.hexdigest()

class R:
    pingtime_cache = {}
    @classmethod
    def get_speed(cls, url):
        assert url and isinstance(url, str)
        import re
        match = re.match('^\w+://([^/]+)/.+$', url)
        assert match, url
        try:
            server = match.group(1)
            if server in cls.pingtime_cache:
                Time = cls.pingtime_cache[server]
            else:
                Time = get_response_time(url)
                print _('Response time of server %(name)s is %(time).1f ms.') % {'name':server, 'time':Time}
        except:
            print _('Server %s does not respond.')%server
            Time = 10000.0
        finally:
            cls.pingtime_cache[server] = Time
            return Time
    @staticmethod
    def compare(u1, u2):
        s1 = R.get_speed(u1)
        s2 = R.get_speed(u2)
        return cmp(s1, s2)
    def sort(self):
        if self.sorted: return
        self.sorted = True
        
        if isinstance(self.url, str): 
            self.sorted_url = [self.url]
        elif isinstance(self.url, list):
            if len(self.url)>1:
                self.url.sort(R.compare)
            self.sorted_url = self.url
        else:
            raise Exception
    def delete_duplicate(self, List):
        ret = []
        servers = set()
        for url in List:
            import re
            match = re.search('://([^/]+)/', url)
            server = match.group(1)
            if not server in servers:
                ret.append(url)
                servers.add(server)
        return ret
    def __init__(self, url_list, size=None, hash=None, filename=None):
        #check url
        assert url_list
        assert isinstance(url_list, (str,list))
        if isinstance(url_list, str): 
            url_list = [ url_list ]
        for e in url_list:
            assert isinstance(e, str), e
            assert e.startswith('http://') or e.startswith('https://') or e.startswith('ftp://')
        #check size
        if size!=None:
            assert size>0
            assert isinstance(size, int) or isinstance(size, long), size
        #check hash
        if hash:
            assert isinstance(hash, str), hash
            assert len(hash)==40, hash

        self.url = self.delete_duplicate(url_list)
        self.size = size
        self.hash = hash
        if filename:
            self.filename = filename
        else:
            if isinstance(url_list, str): u = url_list
            elif isinstance(url_list, list): u = url_list[0]
            import re
            self.filename = re.match('^.+/(.+)$', u).group(1)
            
        self.sorted = False
    @classmethod
    def create_tmp_dir(cls):
        dir = '/var/cache/ailurus/'
        import os
        if not os.path.exists(dir):
            gksudo('mkdir %s -p'%dir)
        own_by_user(dir)
    def check(self, path):
        if self.size:
            import os
            filesize=os.path.getsize(path)
            if filesize!=self.size: 
                raise CommandFailError('File is broken. Expected file length is %s, but real length is %s.'%(self.size, filesize) )
        if self.hash:
            print _('Checking file integrity ...'),
            filehash = sha1(path)
            if filehash!=self.hash: 
                raise CommandFailError('File is broken. Expected hash is %s, but real hash is %s.'%(self.hash, filehash) )
            print _('Good.')
    def download(self):
        self.sort()
        dest = '/var/cache/ailurus/'+self.filename
        import os, sys, traceback
        assert isinstance(self.sorted_url, list)
        for i, url in enumerate(self.sorted_url):
            print '\x1b[1;36m', _('Using mirror %(i)s. There are a total of %(total)s mirrors.') % {'i' : i+1, 'total' : len(self.sorted_url)}, '\x1b[m'
            assert isinstance(url, str)
            try:
                R.create_tmp_dir()
                wget(url, dest)
                self.check(dest)
                return dest
            except:
                traceback.print_exc(file=sys.stderr)
        
        raise CommandFailError(self.url)

class ETCEnvironment:
    def __init__(self):
        self.keys = []
        self.values = {}
        f = open('/etc/environment')
        for line in f:
            items = line.split('=',1)
            if len(items)<2: continue
            key = items[0].strip()
            if not key in self.keys:
                self.keys.append(key)
            value = items[1].strip()
            if value[0]==value[-1]=='\'' or value[0]==value[-1]=='\"': value = value[1:-1]
            self.values[key] = value.split(':')
    def add(self, key, *values):
        assert key and isinstance(key, str),    key
        
        values = list(values)
        assert values
        for v in values:
            assert v and isinstance(v, str),    v
            assert not ':' in v,     v
        
        if not key in self.keys:
            self.keys.append(key)
            self.values[key] = values
        else:
            self.values[key] = values+self.values[key]
    def remove(self, key, *values):
        assert key and isinstance(key, str),    key
        assert values
        for v in values:
            assert v and isinstance(v, str),    v
            assert not ':' in v,     v

        if not key in self.keys: return
        if not values: 
            # delete it directly
            self.keys.remove(key)
            del self.values[key]
        else:
            List = self.values[key]
            self.values[key] = [e for e in List if not e in values]
    def save(self):
        with TempOwn('/etc/environment') as o:
            f = open('/etc/environment', 'w')
            for key in self.keys:
                if not self.values[key]: continue
                f.write(key)
                f.write('=')
                f.write('\"')
                f.write(':'.join(self.values[key]))
                f.write('\"')
                f.write('\n')

class Chdir:
    def __init__(self,path):
        is_string_not_empty(path)
        if path[0]=='-':
            raise ValueError
        import os
        if not os.path.exists(path):
            raise ValueError
        
        self.oldpath = os.getcwd()
        os.chdir(path)
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        import os
        os.chdir(self.oldpath)

def create_file(path, content):
    with TempOwn(path) as o:
        with open(path, 'w') as f:
            f.write(content)

def run_in_new_terminal(file_name):
    import subprocess
    task = subprocess.Popen('LANG=C xterm -T "Ailurus Terminal" -e bash %s'%file_name, shell=True )
    if task.wait():
        raise CommandFailError

class Tasksel:
    fresh_cache = False
    set1 = set()
    set2 = set()
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if cls.fresh_cache: return
        cls.fresh_cache = True
        cls.set1 = set()
        cls.set2 = set()
        s = get_output('tasksel --list-tasks', ignore_error=True)
        for line in s.split('\n'):
            if len(line) == 0: break
            name = line.split()[1]
            if line[0] == 'i':
                cls.set1.add(name)
            elif line[0] == 'u':
                cls.set2.add(name)
    @classmethod
    def install_tasksel_package(cls):
        if not APT.installed('tasksel'):
            APT.install('tasksel')
    @classmethod
    def installed(cls, name):
        is_string_not_empty(name)
        cls.refresh_cache()
        return name in cls.set1
    @classmethod
    def exists(cls, name):
        is_string_not_empty(name)
        cls.refresh_cache()
        return name in cls.set1 or name in cls.set2
    @classmethod
    def get_packages(cls, name):
        ret = []
        output = get_output('tasksel --task-packages '+name)
        for e in output.split():
            if e: ret.append(e)
        return ret
    @classmethod
    def install(cls, name):
        is_string_not_empty(name)
        cls.install_tasksel_package()
        APT.install( *cls.get_packages(name) )
        cls.cache_changed()
    @classmethod
    def remove(cls, name):
        print '\x1b[1;36m', _('Inspecting safely deletable packages. Please wait for a few minutes.') ,'\x1b[m'
        import os
        path = os.path.dirname(os.path.abspath(__file__)) + '/support/safely_deletable_pkgs.py'
        command = ['python', path]
        command.extend(cls.get_packages(name))
        import subprocess
        task = subprocess.Popen(command, stdout=subprocess.PIPE)
        to_remove = []
        for line in task.stdout:
            to_remove.append(line.strip())
        if to_remove:
            APT.remove( *to_remove )
            cls.cache_changed()
