class Product:
    def __init__(self, name, tags=[]):
        self.name = name
        if tags is None:
            self.tags = []
        else:
            self.tags = tags

    def add_tag(self, tag):
        self.tags.append(tag)

    def __str__ (self):
        return f"Product {self.name}, Tags: {', '.joinself.tags}"


if __name__ == "__main__":
    product = Product("Laptop")
    product2 = Product("Smartphone")

    print(product)
    print(product2)

