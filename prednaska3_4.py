class Button:
    def __call__(self, x):
        print(f"Stisknute tlacitko {x}")

def my_click(x):
    print(f"kliknuti bylo zaznameno na {x}")

def process_click(callback):
    #print("Zpracovzni")
    callback(2)
    #print("Zpracovano")

if __name__== "__main__":
    process_click(my_click)
    process_click(lambda x: print(f"kliknuti pres lambda funkce na {x}"))
    process_click(Button())