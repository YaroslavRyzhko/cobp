class MyContext:
    def __init__(self, filename):
        self.filename = filename
        self.fp = None


    def read(self):
        fp = open(self.filename, "r")
        return ""
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type == FileNotFoundError:
            print(f"Soubor {self.filename} nenalezen")
        
        if exc_type is not None:
            print(f"Doslo k chybe {exc_type}")
        return True

if __name__ == "__main__":
    with MyContext("soubor.txt") as context:
        print(context.read())