#!/usr/bin/python

import sys, os, re

def print_traceback():
    import sys, traceback
    traceback.print_exc(file = sys.stderr)

class firefox:
    prefs_js_path = '/home/ds/.mozilla/firefox/5y7bqw54.default/prefs.js'
    prefs_js_line_pattern = re.compile(r'''^user_pref\( # begin
        (['"][^'"]+['"]) # key
        ,\s
        ([^)]+) # value
        \); # end ''', re.VERBOSE)
    key2value = {} # key is native python constant. value is native python constant.
    @classmethod
    def all_user_pref_lines(cls, content):
        assert isinstance(content, (str, unicode))
        lines = content.splitlines()
        ret = []
        for line in lines:
            if line.startswith('user_pref(') and line.endswith(');'):
                ret.append(line)
        return ret
    @classmethod
    def get_key_value_from(cls, user_pref_line): # may raise exception
        'return (key, value). both of them are native python constant.'
        assert isinstance(user_pref_line, (str, unicode))
        match = cls.prefs_js_line_pattern.match(user_pref_line)
        assert match, user_pref_line
        key = match.group(1)
        key = eval(key)
        value = match.group(2)
        true = True # javascript boolean
        false = False # javascript boolean
        value = eval(value)
        return key, value
    @classmethod
    def load_user_prefs(cls):
        cls.key2value.clear()
        with open(cls.prefs_js_path) as f:
            content = f.read()
        lines = cls.all_user_pref_lines(content)
        for line in lines:
            try:
                key, value = cls.get_key_value_from(line)
                cls.key2value[key] = value
            except:
                print_traceback()
    @classmethod
    def get(cls, key):
        'key should be native python string. return native python constant'
        assert isinstance(key, (str, unicode))
        if key in cls.key2value: return cls.key2value[key]
        else: return ''
    @classmethod
    def set(cls, key, value):
        'value should be native python variable'
        cls.key2value[key] = value
    @classmethod
    def save_user_prefs(cls):
        keys = cls.key2value.keys()
        keys.sort()
        with open(cls.prefs_js_path, 'w') as f:
            for key in keys:
                value = cls.key2value[key]
                repr_key = repr(key)
                repr_value = repr(value)
                if value == True: repr_value = 'true'
                elif value == False: repr_value = 'false'
                line = 'user_pref(%s, %s);' % (repr_key, repr_value)
                print >>f, line

firefox.load_user_prefs()
firefox.set('zzz1', 1.1)
firefox.set('zzz2', '2')
firefox.set('zzz3', True)
firefox.save_user_prefs()
firefox.load_user_prefs()
assert firefox.get('zzz1') == 1.1
assert firefox.get('zzz2') == '2'
assert firefox.get('zzz3') == True
