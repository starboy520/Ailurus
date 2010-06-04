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

D = '/usr/share/ailurus/data/'
import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)

def row(text, value, icon=D+'umut_icons/i_default.png', tooltip = None):
    return (text, value, icon, tooltip)

class I:
    this_is_an_installer = True
    def self_check(self):
        'Check errors in source code'
    def install(self):
        raise NotImplementedError
    def installed(self):
        raise NotImplementedError
    def remove(self):
        raise NotImplementedError

class C:
    this_is_a_cure = True
    MUST_FIX, SUGGESTION = range(2)
    type = SUGGESTION
    detail = ''
    def exists(self):
        raise NotImplementedError
    def cure(self):
        raise NotImplementedError
    
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
    def set_query_before_exit(cls, value):
        cls.set_bool('query_before_exit', value)
    @classmethod
    def get_query_before_exit(cls):
        try:       return cls.get_bool('query_before_exit')
        except:    return True
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
    def set_show_software_icon(cls, value):
        cls.set_bool('show_software_icon', value)
    @classmethod
    def get_show_software_icon(cls):
        try: value = cls.get_bool('show_software_icon')
        except: value = True
        return value
    @classmethod
    def set_default_pane(cls, value):
        cls.set_string('default_pane', value)
    @classmethod
    def get_default_pane(cls):
        try: value = cls.get_string('default_pane')
        except: value = 'SystemSettingPane'
        return value
    @classmethod
    def get_locale(cls):
        import locale
        try:
            value = locale.getdefaultlocale()[0]
            if value: return value # language code and encoding may be None if their values cannot be determined.
            else: return 'en_US'
        except ValueError: # may raise exception: "unknown locale"
            print_traceback()
            return 'en_US'
    @classmethod
    def is_Chinese_locale(cls):
        return cls.get_locale().startswith('zh')
    @classmethod
    def is_Poland_locale(cls):
        return cls.get_locale().startswith('pl')
    @classmethod
    def is_Ubuntu(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): 
            return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'Ubuntu' in c
    @classmethod
    def get_Ubuntu_version(cls):
        '''return 'hardy', 'intrepid', 'jaunty', 'karmic' or 'lucid'.'''
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_CODENAME='):
                return line.split('=')[1].strip()
    @classmethod
    def is_Mint(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'LinuxMint' in c
    @classmethod
    def get_Mint_version(cls):
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_RELEASE='):
                a = line.split('=')[1].strip()
        return a
    @classmethod
    def is_YLMF(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): 
            return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'Ylmf_OS' in c
    @classmethod
    def get_YLMF_version(cls):
        '''return 'hardy', 'intrepid', 'jaunty', 'karmic' or 'lucid'.'''
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_CODENAME='):
                return line.split('=')[1].strip()
    @classmethod
    def is_Deepin(cls): # Linux Deepin is based on XUbuntu karmic
        import platform
        return platform.dist()[0] == 'Deepin'
    @classmethod
    def get_Deepin_version(cls):
        'return karmic'
        import platform
        return platform.dist()[2]
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
    def is_ArchLinux(cls): # There is no get_arch_version, since ArchLinux has no version.
        import os
        return os.path.exists('/etc/arch-release')
    @classmethod
    def is_GNOME(cls):
        if cls.is_XFCE(): return False
        try:
            get_output('pgrep -u $USER gnome-panel')
            return True
        except:
            return False
    @classmethod
    def is_KDE(cls):
        try:
            get_output('pgrep -u $USER kdeinit')
            return True
        except:
            try:
                get_output('pgrep -u $USER kdeinit4')
                return True
            except: pass
        return False
    @classmethod
    def is_XFCE(cls):
        try:  
            get_output('pgrep -u $USER xfce4-session')
            return True
        except: 
            return False


def install_locale():
    import gettext
    gettext.translation('ailurus', '/usr/share/locale', fallback=True).install(names=['ngettext'])

def is_legal_license(license):
    return license in [GPL, LGPL, EPL, MPL, BSD, MIT, CDDL, APL, AL] 

def DUAL_LICENSE(A, B):
    assert is_legal_license(A) and is_legal_license(B)
    return _('Dual-licensed under %(A)s and %(B)s') % {'A':A, 'B':B}

def TRI_LICENSE(A, B, C):
    assert is_legal_license(A) and is_legal_license(B) and is_legal_license(C)
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
            print_traceback()
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
            print_traceback()
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

class CommandFailError(Exception):
    'Fail to execute a command'

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

def get_dbus_daemon_version():
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    ret = obj.get_version(dbus_interface='cn.ailurus.Interface')
    return ret    

def restart_dbus_daemon():
    authenticate()
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    obj.exit(dbus_interface='cn.ailurus.Interface')

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
    if os.getuid()==0:
        run(cmd, ignore_error)
        return
    
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
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            run_as_root('mkdir "%s"'%dirname)
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
    # title must not be empty. 
    # otherwise, this error happens. notify_notification_update: assertion `summary != NULL && *summary != '\0'' failed
    assert isinstance(title, str) and title
    assert isinstance(content, str)
    try:
        import pynotify
        if not hasattr(notify,'ailurus_notify'):
            notify.ailurus_notify = pynotify.Notification(' ',' ')
        icon = D+'suyun_icons/notify-icon.png'
        if title == notify.ailurus_notify.get_property('summary'):
            notify.ailurus_notify = pynotify.Notification(title, content, icon)
            notify.ailurus_notify.set_hint_string("x-canonical-append", "")
        else:
            notify.ailurus_notify.update(title, content, icon)
               
        notify.ailurus_notify.set_timeout(10000)
        notify.ailurus_notify.show()
    except:
        print_traceback()

def is32():
    import os
    return os.uname()[-1] != 'x86_64'

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
    try:
        obj.run(string, packed_env_string(), secret_key, False, timeout=36000, dbus_interface='cn.ailurus.Interface')
    except dbus.exceptions.DBusException, e:
        if e.get_dbus_name() == 'cn.ailurus.AccessDeniedError': raise AccessDeniedError
        else: raise

class RPM:
    fresh_cache = False
    __set1 = set()
    __set2 = set()
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if cls.fresh_cache: return
        cls.fresh_cache = True
        cls.__set1 = set()
        cls.__set2 = set()
        import subprocess, os
        path = os.path.dirname(os.path.abspath(__file__)) + '/support/dump_rpm_installed.py'
        task = subprocess.Popen(['python', path],
            stdout=subprocess.PIPE,
            )
        for line in task.stdout:
            cls.__set1.add(line.strip())
        task.wait()
        path = os.path.dirname(os.path.abspath(__file__)) + '/support/dump_rpm_existing.py'
        task = subprocess.Popen(['python', path],
            stderr=subprocess.PIPE, # must be stderr
            )
        for line in task.stderr: # must be stderr
            cls.__set2.add(line.strip())
        task.wait()
    @classmethod
    def get_installed_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__set1
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__set2
    @classmethod
    def exist(cls, package_name):
        cls.refresh_cache()
        return package_name in cls.__set1 or package_name in cls.__set2
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
    apt_get_update_is_called = False
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
        task.wait()
    @classmethod
    def get_installed_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__set1
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__set2
    @classmethod
    def get_autoremovable_pkgs(cls):
        ret = []
        import subprocess, os
        path = os.path.dirname(os.path.abspath(__file__))+'/support/dump_apt_autoremovable.py'
        task = subprocess.Popen(['python', path], stdout=subprocess.PIPE)
        class EndOfStream:
            pass
        def readline(stream):
            line = stream.readline()
            if len(line) == 0: raise EndOfStream
            return line.strip()
        try:
            while True:
                name = readline(task.stdout)
                size = readline(task.stdout)
                size = long(size)
                summary = readline(task.stdout)
                ret.append([name, size, summary,])
        except EndOfStream:
            pass
        task.wait()
        return ret
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
        is_pkg_list(packages)
        if cls.apt_get_update_is_called == False:
            cls.apt_get_update()
        print '\x1b[1;32m', _('Installing packages:'), ' '.join(packages), '\x1b[m'
        # use "force-yes" because playonlinux repository has no gpg key, we want to install it without key.
        run_as_root_in_terminal('apt-get install -y --force-yes ' + ' '.join(packages))
        APT.cache_changed()
        failed = [p for p in packages if not APT.installed(p)]
        if failed:
            msg = 'Cannot install "%s".' % ' '.join(failed)
            raise CommandFailError(msg)
    @classmethod
    def remove(cls, *packages):
        is_pkg_list(packages)
        print '\x1b[1;31m', _('Removing packages:'), ' '.join(packages), '\x1b[m'
        packages = [p for p in packages if APT.installed(p)]
        run_as_root_in_terminal('apt-get remove -y ' + ' '.join(packages))
        APT.cache_changed()
        failed = [p for p in packages if APT.installed(p)]
        if failed:
            msg = 'Cannot remove "%s".' % ' '.join(failed)
            raise CommandFailError(msg)
    @classmethod
    def apt_get_update(cls):
        # (c) 2005-2007 Canonical, GPL
        print '\x1b[1;36m', _('Run "apt-get update". Please wait for few minutes.'), '\x1b[m'
        run_as_root_in_terminal('apt-get update')
        cls.apt_get_update_is_called = True
        cls.cache_changed()
    @classmethod
    def get_deb_depends(cls, filename):
        is_pkg_list([filename])
        import os, re
        if not filename.endswith('.deb'): raise ValueError
        if not os.path.exists(filename): raise ValueError
        output = get_output('LANG=C dpkg --info %s' % filename)
        match=re.search('Depends: (.*)', output)
        if match is None: # no depends 
            return [] 
        items=match.group(1).split(',')
        depends = []
        for item in items:
            depends.append(item.split()[0])
        return depends
    @classmethod
    def install_local(cls, *packages):
        is_pkg_list(packages)
        for package in packages:
            import os
            if not package.endswith('.deb'): raise ValueError
            if not os.path.exists(package): raise ValueError
            depends = cls.get_deb_depends(package)
            if len(depends):
                cls.install(*depends)
            run_as_root_in_terminal('dpkg --install --force-architecture %s'%package)
            cls.cache_changed()

class PACMAN:
    fresh_cache = False
    pacman_sync_called = False
    __pkgs = set()
    __allpkgs = set()
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if getattr(cls, 'fresh_cache', False): return
        cls.fresh_cache = True
        cls.__pkgs = set()
        cls.__allpkgs = set()
        import subprocess, os
        #get installed package names
        task = subprocess.Popen(['pacman', '-Q'],
            stdout=subprocess.PIPE,
            )
        for line in task.stdout:
            cls.__pkgs.add(line.split()[0])
        task.wait()
        #get all existing package names
        task = subprocess.Popen(['pacman', '-Sl'],
            stdout=subprocess.PIPE,
            )
        for line in task.stdout:
            cls.__allpkgs.add(line.split()[1])
        task.wait()
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        return cls.__allpkgs
    @classmethod
    def installed(cls, package_name):
        is_pkg_list([package_name])
        cls.refresh_cache()
        return package_name in cls.__pkgs
    @classmethod
    def install(cls, *package):
        is_pkg_list(packages)
        if not cls.pacman_sync_called:
            cls.pacman_sync()
        print '\x1b[1;32m', _('Installing packages:'), ' '.join(packages), '\x1b[m'
        run_as_root_in_terminal('pacman -S --noconfirm %s' % ' '.join(package))
        cls.cache_changed()
        failed = [p for p in packages if not PACMAN.installed(p)]
        if failed:
            msg = 'Cannot install "%s".' % ' '.join(failed)
            raise CommandFailError(msg)
    @classmethod
    def install_local(cls, path):
        assert isinstance(path, str)
        import os
        assert os.path.exists(path)
        run_as_root_in_terminal('pacman -U --noconfirm %s' % path)
        cls.cache_changed()
    @classmethod
    def remove(cls, *package):
        is_pkg_list(packages)
        print '\x1b[1;31m', _('Removing packages:'), ' '.join(packages), '\x1b[m'
        packages = [p for p in packages if PACMAN.installed(p)]
        run_as_root_in_terminal('pacman -R --noconfirm %s' % ' '.join(package))
        cls.cache_changed()
        failed = [p for p in packages if PACMAN.installed(p)]
        if failed:
            msg = 'Cannot remove "%s".' % ' '.join(failed)
            raise CommandFailError(msg)
    @classmethod
    def pacman_sync():
        print '\x1b[1;36m', _('Run "pacman -Sy". Please wait for a few minutes.'), '\x1b[m'
        run_as_root_in_terminal('pacman -Sy')
        cls.pacman_sync_called = True

def get_response_time(url):
    is_string_not_empty(url)

    import urllib2
    import time
    import sys
    begin = time.time()
    if sys.version_info[:2]>(2,5): # for python 2.6+
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
                print_traceback()
        cls.task_list = []

def download(url, filename):
    is_string_not_empty(url)
    assert url[0]!='-'
    is_string_not_empty(filename)
    assert filename[0]!='-'
    try:
        timeout = Config.wget_get_timeout()
        tries = Config.wget_get_triesnum()

        run("wget --timeout=%(timeout)s --tries=%(tries)s '%(url)s' -O '%(filename)s'"
            %{'timeout':timeout, 'tries':tries, 'url':url, 'filename':filename} )
    except:
        import os
        if os.path.exists(filename): os.unlink(filename)
        raise
    
def reset_dir():
    import os, sys
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

class APTSource2:
    re_pattern_server = None
    re_pattern_url = None
    @classmethod
    def all_conf_files(cls):
        import glob, os
        ret = glob.glob('/etc/apt/sources.list.d/*.list')
        if os.path.exists('/etc/apt/sources.list'):
            ret.append('/etc/apt/sources.list')
        return ret
    @classmethod
    def iter_all_lines(cls):
        for file in cls.all_conf_files():
            f = open(file)
            for line in f:
                yield line
            f.close()
    @classmethod
    def all_lines(cls):
        ret = []
        for file in cls.all_conf_files():
            with open(file) as f:
                ret.extend(f.readlines())
        return ret
    @classmethod
    def all_lines_contain(cls, snip):
        snip = cls.remove_comment(snip)
        for line in cls.iter_all_lines():
            if snip in line: return True
        return False
    @classmethod
    def all_lines_contain_all_of(cls, many_snips):
        for snip in many_snips:
            if not cls.all_lines_contain(snip): return False
        return True
    @classmethod
    def add_lines_to_file(cls, lines, file_path = '/etc/apt/sources.list'):
        assert isinstance(lines, list)
        assert isinstance(file_path, str)
        
        with TempOwn(file_path) as o:
            with open(file_path) as f:
                contents = f.readlines()
            if len(contents) and not contents[-1].endswith('\n'):
                contents.append('\n')
            contents.extend(lines)
            with open(file_path, 'w') as f:
                f.writelines(contents)
    @classmethod
    def remove_snips_from(cls, snips, file_path):
        assert isinstance(snips, list)
        assert isinstance(file_path, str)
        
        with open(file_path) as f:
            contents = f.readlines()
        changed = False
        for i, line in enumerate(contents):
            line = cls.remove_comment(line)
            for snip in snips:
                snip = cls.remove_comment(snip)
                if snip in cls.remove_comment(line):
                    contents[i] = ''
                    changed = True
                    break
        if changed:
            with TempOwn(file_path) as o:
                with open(file_path, 'w') as f:
                    f.writelines(contents)
    @classmethod
    def remove_snips_from_all_files(cls, snips):
        assert isinstance(snips, list)
        for file_path in cls.all_conf_files():
            cls.remove_snips_from(snips, file_path)
    @classmethod
    def remove_comment(cls, line):
        return line.split('#', 1)[0].strip()
    @classmethod
    def is_official_line(cls, line):
        line = cls.remove_comment(line)
        for snip in ['-backports', '-proposed', '-security', '-updates']:
            snip = VERSION + snip
            if snip in line: return True
        return False
    @classmethod
    def get_server_from_line(cls, line):
        line = cls.remove_comment(line)
        import re
        if cls.re_pattern_server is None:
            cls.re_pattern_server = re.compile(r'^deb(-src)? [a-z]+://([^/]+)/.*$')
        match = cls.re_pattern_server.match(line)
        if match: return match.group(2)
        else:     return None
    @classmethod
    def get_url_from_line(cls, line):
        line = cls.remove_comment(line)
        import re
        if cls.re_pattern_url is None:
            cls.re_pattern_url = re.compile(r'^deb(-src)? (\S+) .*$')
        match = cls.re_pattern_url.match(line)
        if match: return match.group(2)
        else:     return None
    @classmethod
    def official_servers(cls):
        ret = set()
        for line in cls.iter_all_lines():
            if cls.is_official_line(line):
                server = cls.get_server_from_line(line)
                ret.add(server)
        return ret
    @classmethod
    def official_urls(cls):
        ret = set()
        for line in cls.iter_all_lines():
            if cls.is_official_line(line):
                url = cls.get_url_from_line(line)
                ret.add(url)
        return ret
    @classmethod
    def third_party_urls(cls):
        offi_urls = cls.official_urls()
        ret = set()
        for line in cls.iter_all_lines():
            url = cls.get_url_from_line(line)
            if url and url not in offi_urls: ret.add(url)
        return ret
    @classmethod
    def all_urls(cls):
        ret = set()
        for line in cls.iter_all_lines():
            url = cls.get_url_from_line(line)
            if url: ret.add(url)
        return ret
    @classmethod
    def this_line_contain(cls, line, snip):
        return snip in cls.remove_comment(line)
    @classmethod
    def this_line_contain_any_of(cls, line, snip_set):
        for snip in snip_set:
            if cls.this_line_contain(line, snip):
                return True
        return False
    @classmethod
    def remove_official_servers(cls):
        offi_servers = cls.official_servers()
        for file in cls.all_conf_files():
            with open(file) as f:
                contents = f.readlines()
            changed = False
            for i, line in enumerate(contents):
                if cls.this_line_contain_any_of(line, offi_servers):
                    contents[i] = ''
                    changed = True
            if changed:
                with TempOwn(file) as o:
                    with open(file, 'w') as f:
                        f.writelines(contents)
    @classmethod
    def add_official_url(cls, url):
        with TempOwn('/etc/apt/sources.list') as o:
            with open('/etc/apt/sources.list') as f:
                contents = f.readlines()
            if len(contents) and not contents[-1].endswith('\n'):
                contents.append('\n')
            contents.append('deb %(url)s %(version)s main restricted universe multiverse\n'
                            'deb %(url)s %(version)s-backports restricted universe multiverse\n'
                            'deb %(url)s %(version)s-proposed main restricted universe multiverse\n'
                            'deb %(url)s %(version)s-security main restricted universe multiverse\n'
                            'deb %(url)s %(version)s-updates main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-backports main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-proposed main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-security main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-updates main restricted universe multiverse\n'
                            % {'url':url, 'version':VERSION})
            with open('/etc/apt/sources.list', 'w') as f:
                f.writelines(contents)

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
    def get_preference_path(cls):
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
        return '%s/%s/'%(path,default_profile_path)
        
    @classmethod
    def get_extensions_path(cls):
        dir = cls.get_preference_path() + '/extensions/'
        import os
        if not os.path.exists(dir): os.mkdir(dir)
        return dir

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
            print_traceback()
    
    @classmethod
    def __get_extensions_basic(cls):
        import os, glob
        try:
            ret = []
            extensions_path = cls.get_extensions_path()
            assert os.path.exists(extensions_path), extensions_path
            extensions = glob.glob('%s/*'%extensions_path)
            for extension in extensions:
                cls.analysis_extension(extension, ret)
            return ret
        except:
            print_traceback()
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
                print_traceback()
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
        import os, sys
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
                print_traceback()
        
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

def print_traceback():
    import sys, traceback
    traceback.print_exc(file = sys.stderr)

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
        task.wait()
        if to_remove:
            APT.remove( *to_remove )
            cls.cache_changed()

def window_manager_name():
    """Returns window manager name"""
    # Thanks to Whise (Helder Fraga), we have this elegant function!
    # This function is from Screenlets/sensors.py
    # GPLv3
    import gtk
    root = gtk.gdk.get_default_root_window()
    try:
        ident = root.property_get("_NET_SUPPORTING_WM_CHECK", "WINDOW")[2]
        _WM_NAME_WIN = gtk.gdk.window_foreign_new(long(ident[0]))
    except TypeError, exc:
        _WM_NAME_WIN = ""

    name = ""
    win = _WM_NAME_WIN
    if (win != None):
        try:
            name = win.property_get("_NET_WM_NAME")[2]
        except TypeError, exc:
            pass
    return name

def get_ailurus_version():
    import os
    path = os.path.dirname(__file__) + '/version'
    with open(path) as f:
        return f.read().strip()
    
def get_ailurus_release_date():
    import os, time
    path = os.path.dirname(__file__) + '/version'
    info = os.stat(path)
    return time.strftime('%Y-%m-%d', time.gmtime(info.st_mtime))

AILURUS_VERSION = get_ailurus_version()
AILURUS_RELEASE_DATE = get_ailurus_release_date()

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
    import pynotify
    pynotify.init('Ailurus')
except:
    print 'Cannot init pynotify'

import random
secret_key = ''.join([chr(random.randint(97,122)) for i in range(0, 64)])

UBUNTU = Config.is_Ubuntu()
UBUNTU_DERIV = False # True value means Ubuntu derivative. For Ubuntu it is False. For Mint it is True.
MINT = Config.is_Mint()
YLMF = Config.is_YLMF()
DEEPIN = Config.is_Deepin()
FEDORA = Config.is_Fedora()
ARCHLINUX = Config.is_ArchLinux()
if UBUNTU:
    VERSION = Config.get_Ubuntu_version()
elif MINT:
    UBUNTU_DERIV = True
    VERSION = Config.get_Mint_version()
    assert VERSION in ['5', '6', '7', '8', '9']
    VERSION = ['hardy', 'intrepid', 'jaunty', 'karmic', 'lucid', ][int(VERSION)-5]
elif YLMF:
    UBUNTU_DERIV = True
    VERSION = Config.get_YLMF_version()
elif DEEPIN:
    UBUNTU_DERIV = True
    VERSION = Config.get_Deepin_version()
elif FEDORA:
    VERSION = Config.get_Fedora_version()
elif ARCHLINUX:
    VERSION = '' # ArchLinux has no version -_-b
else:
    print _('Your Linux distribution is not supported. :(')
    VERSION = ''

GNOME = False
KDE = False
XFCE = False
# Thank you, GShutdown Team!
# This code is from gshutdown/src/values.c
# GPLv2
WINDOW_MANAGER = window_manager_name()
if WINDOW_MANAGER == "Metacity":
    GNOME = True
elif WINDOW_MANAGER == "KWin":
    KDE = True
elif WINDOW_MANAGER == "Xfwm4":
    XFCE = True
else:
    print 'Window Manager is not recognized:', WINDOW_MANAGER
    # These functions are less effective, but they work.
    GNOME = Config.is_GNOME()
    KDE = Config.is_KDE()
    XFCE = Config.is_XFCE()
