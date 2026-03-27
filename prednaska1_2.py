prihlaseny_uzivatel = None

def pouze_prihl(func):
    def wrapper():
        if prihlaseny_uzivatel is None:
            return None
        return func()
    return wrapper

@pouze_prihl
def vypis_informace():
    print("Tajne informace")

@pouze_prihl
def vykresli_obrazek():
    print("+----+")
    print("+  *  +")
    print("+----+")
    
if __name__ == "__main__":
    prihlaseny_uzivatel = 'Bob'
    vypis_informace()
    vykresli_obrazek()