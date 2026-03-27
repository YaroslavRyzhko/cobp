class spatnaCastka(Exception):
    pass

class BankovniUcet:
    def __init__ (self):
        self.__zustatek = 0

    @property
    def zustatek(self):
        return self.__zustatek

    @zustatek.setter
    def zustatek(self, castka):
        if castka < 0:
            raise spatnaCastka('Nemuzeme ulozit zaporny zustatek')
        self.__zustatek = castka

    def __str__(self):
        return f"Bankovni ucet zustatek = {self.zustatek})"
    
if __name__ == "__main__":
    ucet = BankovniUcet()
    try:
        ucet.zustatek = 150
    except:
        print("chyba pri ukladani")
    print(ucet.zustatek)