from lib import *

class Random_state(I):
    category = 'browser'
    def install(self): pass
    def remove(self): pass
    def installed(self):
        import random
        v = random.randint(0, 1)
        return bool(v)