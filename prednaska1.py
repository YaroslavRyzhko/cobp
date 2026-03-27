class BankovniUcet:
    def __init__ (self, majitel):
        self.majitel = majitel
        self.__zustatek = 0

    @property
    def zustatek(self):
        return self.__zustatek

    def vkald(self, castka):
        if castka < 0:
            raise RuntimeError('vkladna castka nemuze byt zaporna')
        self.__zustatek += castka

    def vyber(self, castka):
        if castka < 0:
            raise RuntimeError('vybrana castka nemuze byt zaporna')
        if castka > self.__zustatek:
            raise RuntimeError('vybrana castka je vyssi nez zustatek')
        self.__zustatek -= castka

    def __str__(self):
        return f"Bankovni ucet(majitel = {self.majitel}, zustatek = {self.zustatek})"
    
class SporiciUcet(BankovniUcet):
    def __init__(self, majitel, urok = 0.1):
        super().__init__(majitel)
        self.urok = urok

    def __str__(self):
        return f"Sporici ucet(majitel = {self.majitel}, zustatek = {self.zustatek}, urok = {self.urok})"

if __name__ == "__main__":
    ucet = SporiciUcet("Jaroslav", 4.0)
    print(ucet)
    ucet.vkald(100)
    print(ucet)
