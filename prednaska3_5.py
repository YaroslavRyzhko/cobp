class Person:

    def __str__(self):
        
        result = ["vypis, informace:"]
        for key, value in self.__dict__.items():
            result.append(f"{key}, {value}")
        return "\n".join(result)
        

if __name__ == "__main__":
    json_data = '"name"'
    
    p = Person("Alice", 30)
    print(p.__dict__)