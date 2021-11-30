import json


class Coin:

    def __init__(self, name):
        self.name = name
    

class Coins:

    def __init__(self):
        self.coins = []
        self.coins_in_names = {}
        
    def v_slovar(self):
        return {
            "coini":[
                {
                    "ime": coin.name,
                }
                for coin in self.coins
            ]
        }

    def add_coin(self, name):
        if name not in self.coins_in_names:
            new = Coin(name)
            self.coins.append(new)
            self.coins_in_names[name] = new
            return new

    @classmethod
    def iz_slovarja(cls, slovar_s_coini):
        coini = cls()
        for coin in slovar_s_coini["coini"]:
            nov_coin = coini.add_coin(
                coin["ime"]
                )
        return coini



    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, "w") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)


    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_s_coini = json.load(datoteka)
        return cls.iz_slovarja(slovar_s_coini)