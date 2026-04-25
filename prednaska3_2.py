def generate_num(n):
    for i in range(n):
        yield i


if __name__ == "__main__":
    for num in generate_num(10):
        print(num)
