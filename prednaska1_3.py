class CislaIterator:
    def __init__(self, maximum):
        self.actual = 0
        self.maximum = maximum
    
    def __next__(self):
        if self.actual > self.maximum:
            raise StopIteration
        tmp = self.actual
        self.actual += 1
        return tmp

class Cisla:
    def __init__(self, max_cislo):
        self.max_cislo = max_cislo

    def __iter__(self):
        return CislaIterator(self.max_cislo)

if __name__ == "__main__":
    cisla = Cisla(5)
    for c in cisla:
        print(c)
    print("Konec")