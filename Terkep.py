class Hazak:
    def __init__(self):
        self.hazak = dict()
        self.hazak['haz1'] = 10010
        self.hazak['haz2'] = 10020
        self.hazak['haz3'] = 10030

    def get_haz(self, haz_name):
        if haz_name in self.hazak.keys():
            return self.hazak[haz_name]
        else:
            return None
