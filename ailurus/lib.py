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
AILURUS_VERSION = '10.04.2.3'
AILURUS_RELEASE_DATE = '2010-04-25'
D = '/usr/share/ailurus/data/'
import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)

class I:
    this_is_an_installer = True
    
class Config:
    @classmethod
    def make_config_dir(cls):
        import os
        dir = os.path.expanduser('~/.config/ailurus/')
        if not os.path.exists(dir): # make directory
            try:    os.makedirs(dir)
            except: pass # directory exists
        if os.stat(dir).st_uid != os.getuid(): # change owner
            run_as_root('chown $USER:$USER "%s"'%dir)
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
    def set_hide_quick_setup_pane(cls, value):
        cls.set_bool('hide_quick_setup_pane', value)
    @classmethod
    def get_hide_quick_setup_pane(cls):
        try:        return cls.get_bool('hide_quick_setup_pane')
        except:     return False
    @classmethod
    def set_disable_tip(cls, value):
        cls.set_bool('disable-tip-on-startup', value)
    @classmethod
    def get_disable_tip(cls):
        try:       return cls.get_bool('disable-tip-on-startup')
        except: return False
    @classmethod
    def set_query_before_exit(cls, value):
        cls.set_bool('query_before_exit', value)
    @classmethod
    def get_query_before_exit(cls):
        try:       return cls.get_bool('query_before_exit')
        except:    return True
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

def install_locale(force_reload=False):
    assert isinstance(force_reload, bool)
    
    if force_reload or getattr(install_locale, 'installed', False)==False:
        install_locale.installed = True
    else: return

    import gettext
    gettext.translation('ailurus', '/usr/share/locale', fallback=True).install(names=['ngettext'])

def DUAL_LICENSE(A, B):
    return _('Dual-licensed under %(A)s and %(B)s') % {'A':A, 'B':B}

def TRI_LICENSE(A, B, C):
    return _('Tri-licensed under %(A)s, %(B)s and %(C)s') % {'A':A, 'B':B, 'C':C}

class ResponseTime:
    map = {}
    changed = False
    @classmethod
    def load(cls):
        import os
        try:
            path = Config.get_config_dir() + 'response_time_2'
            if not os.path.exists(path): return
            with open(path) as f:
                lines = f.readlines()
            for i in range(0, len(lines), 2):
                url = lines[i].strip()
                time = float(lines[i+1].strip())
                cls.map[url] = time
        except IOError:
            import traceback
            traceback.print_exc()
    @classmethod
    def save(cls):
        if not cls.changed: return
        try:
            path = Config.get_config_dir() + 'response_time_2'
            with open(path, 'w') as f:
                for key, value in cls.map.items():
                    print >>f, key
                    print >>f, value
        except IOError:
            import traceback
            traceback.print_exc()
    @classmethod
    def get(cls, url):
        is_string_not_empty(url)
        return cls.map[url]
    @classmethod
    def set(cls, url, value):
        is_string_not_empty(url)
        assert isinstance(value, (int,float)) and value > 0
        cls.map[url] = value
        cls.changed = True

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
        new_args.append(AILURUS_VERSION)
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

def spawn_as_root(command):
    is_string_not_empty(command)
    
    authenticate()
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    obj.spawn(command, packed_env_string(), secret_key, dbus_interface='cn.ailurus.Interface')

def drop_priviledge():
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    obj.drop_priviledge(secret_key, dbus_interface='cn.ailurus.Interface')
    
class AccessDeniedError(Exception):
    'User press cancel button in policykit window'

def run_as_root(cmd, ignore_error=False):
    is_string_not_empty(cmd)
    assert isinstance(ignore_error, bool)
    
    import os
    if os.getuid()!=0:
        print '\x1b[1;33m', _('Run command:'), cmd, '\x1b[m'
        authenticate()
        import dbus
        bus = dbus.SystemBus()
        obj = bus.get_object('cn.ailurus', '/')
        try:
            obj.run(cmd, packed_env_string(), secret_key, ignore_error, timeout=36000, dbus_interface='cn.ailurus.Interface')
        except dbus.exceptions.DBusException, e:
            if e.get_dbus_name() == 'cn.ailurus.AccessDeniedError': raise AccessDeniedError
            else: raise
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
    
class TempOwn:
    def __init__(self,path):
        is_string_not_empty(path)
        if path[0]=='-':
            raise ValueError
        import os
        if not os.path.exists(path):
            run_as_root('touch "%s"'%path)
        run_as_root('chown $USER:$USER %s'%path )
        self.path = path
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        run_as_root('chown root:root %s'%self.path)

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
            run_as_root('chown $USER:$USER "%s"'%path)

def is_pkg_list(packages):
    if not len(packages): raise ValueError
    for package in packages:
        is_string_not_empty(package)
        if package[0]=='-': raise ValueError
        if ' ' in package: raise ValueError

def run_as_root_in_terminal(command):
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
    obj.run(string, packed_env_string(), secret_key, False, timeout=36000, dbus_interface='cn.ailurus.Interface')

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
        run_as_root_in_terminal('yum install %s -y' % ' '.join(package))
        cls.cache_changed()
    @classmethod
    def install_local(cls, path):
        assert isinstance(path, str)
        import os
        assert os.path.exists(path)
        
        run_as_root_in_terminal('yum localinstall --nogpgcheck -y %s' % path)
        cls.cache_changed()
    @classmethod
    def remove(cls, *package):
        run_as_root_in_terminal('yum remove %s -y' % ' '.join(package))
        cls.cache_changed()
    @classmethod
    def import_key(cls, path):
        assert isinstance(path, str)
        run_as_root_in_terminal('rpm --import %s' % path)

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
        all_packages = packages
        packages = [ e for e in packages if not APT.installed(e) ]
        if packages:
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
            print '\x1b[1;32m', _('Installing packages:'), ' '.join(packages), '\x1b[m'
            # run command
            run_as_root(' '.join(cmd))
            # notify change
            APT.cache_changed()
        # check state
        failed = []
        for p in all_packages:
            if not APT.installed(p): failed.append(p)
        if failed:
            msg = 'Cannot install "%s".' % ' '.join(failed)
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
            run_as_root(' '.join(cmd))
            # notify change
            APT.cache_changed()
        # check state
        failed = []
        for p in packages:
            if APT.installed(p): failed.append(p)
        if failed or not_exist:
            msg = 'Cannot remove "%s".' % ' '.join(failed+not_exist)
            raise CommandFailError(msg)
    @classmethod
    def apt_get_update(cls):
        # (c) 2005-2007 Canonical, GPL
        print '\x1b[1;36m', _('Run "apt-get update". Please wait for few minutes.'), '\x1b[m'
        cmd = "/usr/sbin/synaptic --hide-main-window --non-interactive -o Synaptic::closeZvt=true --update-at-startup"
        run_as_root(cmd, ignore_error=True)
        cls.updated = True
        cls.cache_changed()

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
            run_as_root('dpkg --install --force-architecture %s'%package)
            APT.cache_changed()
    @classmethod
    def remove_deb(cls, package_name):
        is_string_not_empty(package_name)
        run_as_root('dpkg -r %s'%package_name)
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

def download(url, filename):
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
        import time
        self.start_time = time.time()
    def elapsed_time(self):
        import time
        return time.time() - self.start_time
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
    def can_download(self):
        import urllib2
        for url in self.url:
            try:
                print url
                f = urllib2.urlopen(url)
                return True
            except:
                pass
        return False
    @classmethod
    def create_tmp_dir(cls):
        dir = '/var/cache/ailurus/'
        import os
        if not os.path.exists(dir):
            run_as_root('mkdir %s -p'%dir)
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
                download(url, dest)
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
        for v in values:
            assert v and isinstance(v, str),    v
            assert not ':' in v,     v

        if not key in self.keys: return
        if not values: 
            # delete it directly
            try:    self.keys.remove(key)
            except: pass
            try:    del self.values[key]
            except: pass
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
        for line in output.split('\n'):
            if line.startswith('W: '): continue # skip warning messages, such as Duplicate sources.list entry
            item = line.strip()
            if item: ret.append(item)
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

def show_about_dialog():
    import gtk
    gtk.about_dialog_set_url_hook( lambda dialog, link: 1 )
    about = gtk.AboutDialog()
    about.set_logo(gtk.gdk.pixbuf_new_from_file(D+'suyun_icons/logo.png'))
    about.set_name('Ailurus')
    about.set_version(AILURUS_VERSION)
    about.set_website_label( _('Ailurus blog')+' http://ailurus.cn/' )
    about.set_website('http://ailurus.cn/')
    about.set_authors( [
          _('Developers:'),
          'Homer Xing <homer.xing@gmail.com>', 
          'CHEN Yangyang <skabyy@gmail.com>',
          'MA Yue <velly.empire@gmail.com>',
          'QI Chengjie <starboy.qi@gmail.com>',
          '',
          _('Contributors:'),
          'HUANG Wei <wei.kukey@gmail.com>',
           ] )
    about.set_translator_credits(_('translator-credits'))
    about.set_artists( [
          'SU Yun',
          'M. Umut Pulat    http://12m3.deviantart.com/', 
          'Andrea Soragna   http://sora-meliae.deviantart.com/',
          'Paul Davey       http://mattahan.deviantart.com/',] )
    about.set_copyright( _(u"Copyright © 2007-2010,\nTrusted Digital Technology Laboratory,\nShanghai Jiao Tong University, China.") )
    about.set_wrap_license(False)
    about.set_license(
'''
Ailurus is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

The source code in Ailurus is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ailurus; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Unlike otherwise indicated, artwork is available under the Creative Commons 
Attribution Share-alike license v3.0 or any later version. To view a copy of 
this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send 
a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco,
California, 94105, USA.

Some Rights Reserved:

The rights in the trademarks, logos, service marks of Canonical Ltd, as well as
the look and feel of Ubuntu, are subject to the Canonical Trademark Policy at
http://www.ubuntu.com/ubuntu/TrademarkPolicy 

All images in directory "data/suyun_icons" are released under the GPL License, 
version 2 or higher version. Their copyright are holded by SU Yun.

All images in directory "data/sona_icons" are released under the GPL License. 
Their copyright are holded by Andrea Soragna.

All images in directory "data/velly_icons" are released under the GPL License. 
Their copyright are holded by MA Yue.

All images in directory "data/umut_icons" and "data/appicons" are are released
under the GNU Lesser General Public License. Their copyright are holded by M. Umut Pulat.

In directory "data/other_icons":
acire.png is copied from Acire project. It is released under the GPL license.
ailurus.png is released under the GPL license. Its copyright is holded by SU Yun.
ailurus_for_splash.png is released under the GPL license. Its copyright is holded by MA Yue.
audacity.png is copied from Audacity project. It is released under the GPL license. Its copyright is holded by Audacity Team.
blank.png is released under the GPL license. Its copyright is holded by Homer Xing.
bluefish.png is copied from Bluefish project. It is released under the GPL license. Its copyright is holded by Olivier Sessink.
bluetooth.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
childsplay.png is copied from Childsplay project. It is released under the GPL license. Its copyright is holded by Stas Zytkiewicz.
codeblocks.png is copied from Code::Blocks project. It is released under the GPL v3.0 license. Its copyright is holded by Code::Blocks Team.
done.png, fail.png, parcellite.png, s_desktop.png, started.png, toolbar_back.png, toolbar_disable.png, toolbar_enable.png, toolbar_forward.png, toolbar_quit.png are copied from GNOME project. They are released under the GPL license. There copyright are holded by GNOME community.
extcalc.png is copied from Extcalc project. It is released under the GPL v2 license. Its copyright is holded by Extcalc Team.
fedora.png is copied from Fedora project. It is released under the GPL v3.0 license. Its copyright is holded by Fedora community.
firestarter.png is copied from Firestarter project. It is released under the GPL license. Its copyright is holded by Tomas Junnonen.
gcompris.png is copied from GCompris project. It is released under the GPL license. Its copyright is holded by Bruno Coudoin.
liferea.png is copied from Liferea project. It is released under the GPL license. Its copyright is holded by Liferea Team.
locale.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
stardict.png is copied from Stardict project. It is released under GPL v3 license. Its copyright is holded by Stardict Team.
m_clean_up.png is released under the GPL license. Its copyright is holded by MA Yue.
netbeans.png is copied from Netbeans project. It is released under the GPL v2 license. Its copyright is holded by Sun Microsystems Ltd.
pitivi.png is copied from PiTiVi project. It is released under the LGPL license. Its copyright is holded by PiTiVi Team.
python.png is copied from Python project. It is released under the Python license. Its copyright is holded by Python Software Foundation.
qtcreator.png is copied from Qt project. It is released under the LGPL license. Its copyright is holded by Nokia Corporation.
s_nautilus.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
songbird.png is copied from Songbird project. It is released under the GPL v2. Its copyright is holded by Songbird Team.
toolbar_study.png is released under the LGPL license. Its copyright is holded by Umut Pulat.
tux.png is released under the LGPL license. Its copyright is holded by Umut Pulat.
tuxpaint.png is copied from Tux Paint project. It is released under the GPL license. Its copyright is holded by Tux Paint Team.
ubuntu.png is copied from Ubuntu project. Its copyright is holded by Canonical Ltd. Some rights reserved: The rights in the trademarks, logos, service marks of Canonical Ltd, as well as the look and feel of Ubuntu, are subject to the Canonical Trademark Policy at http://www.ubuntu.com/ubuntu/TrademarkPolicy 
vuze.png is copied from Vuze project. It is released under the GPL license. Its copyright is holded by Vuze Team.
wallpaper-tray.png is copied from Wallpaper Tray project. It is released under the GPL license. Its copyright is holded by Wallpaper Tray Team.
worldofpadman.png is copied from World of Padman project. It is realeased under the GPL license.
xbmc.png is copied from XBMC project. It is released under the GPL license. Its copyright is holded by XBMC Team.
All rights of other images which are not mensioned above are preserves by their authors.

All rights of the applications installed by Ailurus are preserved by their authors.''')
    about.vbox.pack_start( gtk.Label( _('Welcome to leave response in blog~') ) , False, False )
    about.vbox.pack_start( gtk.Label( _('\nThis version is released at %s.') % AILURUS_RELEASE_DATE), False)
    about.vbox.show_all()
    about.run()
    about.destroy()

def show_special_thank_dialog():
    import StringIO
    text = StringIO.StringIO()
    print >>text, _('We wish to express thankfulness to these projects:')
    print >>text, '<b><big>Lazybuntu, UbuntuAssistant'
    print >>text, 'GTweakUI, Easy Life, Ubuntu-tweak, CPU-G</big></b>'
    print >>text
    print >>text, _('We sincerely thank these people:')
    print >>text
    print >>text, _('The people who provide inspiration:')
    print >>text, '<b><big>PCMan, Careone, novia, '
    print >>text, 'BAI Qingjie, Aron Xu, Federico Vera, '
    print >>text, 'ZHU Jiandy, Maksim Lagoshin, '
    print >>text, 'Romeo-Adrian Cioaba, David Morre, '
    print >>text, 'Liang Suilong, Lovenemesis, Chen Lei, '
    print >>text, 'DaringSoule, Ramesh Mandaleeka</big></b>'
    print >>text
    print >>text, _('The people who designs the logo:')
    print >>text, '<b><big>SU Yun</big></b>'
    print >>text
    print >>text, _('The people who maintain PPA repository:')
    print >>text, '<b><big>Aron Xu</big></b>'
    print >>text
    print >>text, _('The people who provide a lot of Linux skills:')
    print >>text, '<b><big>Oneleaf</big></b>'
    print >>text
    print >>text, _('The people who provide a lot of Debian packages:')
    print >>text, '<b><big>Careone</big></b>'
    print >>text
    print >>text, _('The people who provide a lot of translation:')
    print >>text, '<b><big>Federico Vera, Sergey Sedov, Sérgio Marques</big></b>', 
    print >>text, _('and many other people.')
    print >>text 
    print >>text, _('The people who report bugs:')
    print >>text, '<b><big>LIU Liang, YU Pengfei, q1ha0,'
    print >>text, 'novia, hardtzh, fegue</big></b>', _('and many other people.')
    print >>text
    print >>text, _('The people who eliminate bugs:')
    print >>text, '<b><big>anjiannian, PES6, eemil.lagerspetz</big></b>'
    print >>text
    print >>text, _('The people who publicize this software:')
    print >>text, '<b><big>dsj, BingZhiGuFeng, chinairaq, coloos,'
    print >>text, 'TombDigger, sudo, Jandy Zhu</big></b>', _('and many other people.')
    print >>text
    print >>text, _('and the people not mensioned here.')
    import gtk
    label = gtk.Label()
    label.set_markup(text.getvalue())
    text.close()
    label.set_justify(gtk.JUSTIFY_CENTER)
    scroll = gtk.ScrolledWindow()
    scroll.add_with_viewport(label)
    scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    scroll.set_shadow_type(gtk.SHADOW_NONE)
    scroll.set_size_request(-1, 500)
    dialog = gtk.Dialog( _('Thanks'), None, 
        gtk.DIALOG_MODAL | 
        gtk.DIALOG_NO_SEPARATOR, 
        buttons = (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
    dialog.set_border_width(10)
    dialog.vbox.pack_start(scroll, False, False)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()

def check_update():
    try:
        OLD_RELEASE_DATE = AILURUS_RELEASE_DATE 
        import gtk
        
        def url_button(url):
            import gtk
            def func(w, url): open_web_page(url)
            def enter(w, e): 
                try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
                except AttributeError: pass
            def leave(w, e): 
                try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
                except AttributeError: pass
            label = gtk.Label()
            label.set_markup("<span color='blue'><u>%s</u></span>"%url)
            button = gtk.Button()
            button.connect('clicked', func, url)
            button.connect('enter-notify-event', enter)
            button.connect('leave-notify-event', leave)
            button.set_relief(gtk.RELIEF_NONE)
            button.add(label)
            align = gtk.Alignment(0, 0.5)
            align.add(button)
            return align
    
        import urllib2
        import re
        if Config.is_Fedora():
            filename_pattern = r'ailurus-[0-9.]+-1\.noarch\.rpm'
            version_pattern = r'ailurus-([0-9.]+)-1\.noarch\.rpm'
            code_url = 'http://homerxing.fedorapeople.org/'
        elif Config.is_Ubuntu():
            version_string = Config.get_Ubuntu_version()
            filename_pattern = r'ailurus_[0-9.]+-0%s1_all\.deb' % version_string
            version_pattern = r'ailurus_([0-9.]+)-0%s1_all\.deb' % version_string
            code_url = 'http://ppa.launchpad.net/ailurus/ppa/ubuntu/pool/main/a/ailurus/'
        else:
            return
        lastest_version = AILURUS_VERSION
        lastest_filename = ''
        f = urllib2.urlopen(code_url)
        for line in f.readlines():
            filenames = re.findall(filename_pattern, line)
            for filename in filenames:
                match = re.search(version_pattern, filename)
                version = match.group(1)
                if version.split('.') > lastest_version.split('.'):
                    lastest_version = version
                    lastest_filename = filename
        f.close()
        import gtk
        dlg = gtk.Dialog('',
                         None, gtk.DIALOG_NO_SEPARATOR,
                         (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))
        vbox = gtk.VBox(False, 5)
        if lastest_filename:
            dlg.set_title(_('A new version is available'))
            label = gtk.Label( _('Version %s is released.\n'
                                 'You can download it from:')
                                 % lastest_version)
            button = url_button(code_url+lastest_filename)
            vbox.pack_start(label)
            vbox.pack_start(button, False)
        else:
            dlg.set_title(_('Check update'))
            label = gtk.Label( _('You have already installed the latest Ailurus version. :)') )
            vbox.pack_start(label)
        image = gtk.Image()
        image.set_from_file(D+'suyun_icons/update.png')
        hbox = gtk.HBox(False, 5)
        hbox.pack_start(image, False)
        hbox.pack_start(vbox, False)
        dlg.vbox.pack_start(hbox, False)
        dlg.vbox.show_all()
        dlg.run()
        dlg.destroy()
    except:
        import traceback
        traceback.print_exc()
    
def show_changelog():
    import gtk
    buffer = gtk.TextBuffer()
    with open('/usr/share/ailurus/ChangeLog') as f:
        buffer.set_text(f.read())
    textview = gtk.TextView()
    textview.set_buffer(buffer)
    textview.set_editable(False)
    textview.set_cursor_visible(False)
    textview.set_wrap_mode(gtk.WRAP_WORD)
    scroll = gtk.ScrolledWindow()
    scroll.add(textview)
    scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    scroll.set_shadow_type(gtk.SHADOW_IN)
    dialog = gtk.Dialog( _('Ailurus changelog'), None, 
                gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR, 
                buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
    dialog.set_border_width(10)
    dialog.vbox.pack_start(scroll)
    dialog.vbox.set_size_request(700, 500)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()


Config.init()

install_locale()

GPL = _('GNU General Public License')
LGPL = _('GNU Lesser General Public License')
EPL = _('Eclipse Public License')
MPL = _('Mozilla Public License')
BSD = _('Berkeley Software Distribution License')
MIT = _('MIT License')
CDDL = _('Common Development and Distribution License')
APL = _('Aptana Public License')
AL = _('Artistic License')

import atexit
atexit.register(ResponseTime.save)
atexit.register(KillWhenExit.kill_all)
atexit.register(drop_priviledge) 

try:
    Config.get_bool('show-a-linux-skill-bubble')
except:
    try:
        Config.set_bool('show-a-linux-skill-bubble', True)
        ShowALinuxSkill.install()
    except:
        import traceback
        traceback.print_exc()
        

import random
secret_key = ''.join([chr(random.randint(97,122)) for i in range(0, 64)])
