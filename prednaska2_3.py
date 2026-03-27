from dataclasses import dataclass

@dataclass(order=True)
class User:
    name: str
    age: int

if __name__ == "__main__":
    user1 = User("Bob", 25)
    user2 = User("Alice", 23)

    users = [user1, user2]
    print(users)

    print(sorted(users))