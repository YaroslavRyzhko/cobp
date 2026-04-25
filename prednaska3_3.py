class Counter:
    def __init__(self, max_val):
        self.max_val = max_val
        self.value = 0

    def __iter__(self):
        x = 0
        while x < self.max_val:
            yield
            x += 1
    
    def __next__(self):
        if self.value < self.max_val:
            current_val = self.value
            self.value += 1
            return current_val
        else:
            raise StopIteration
        
if __name__ == "__main__":
    counter = Counter(10)
    it1 = iter(counter)
    it2 = iter(counter)
    print(next(it1))
    print(next(it1))
    print(next(it2))
    print(next(it2))
    print(next(it1))