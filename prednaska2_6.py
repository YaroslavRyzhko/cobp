from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

if __name__ == "__main__":
    user = User(id="1", name="Yaroslav", email = "yar@gmail.com")
    json_data = user.model_dump_json()
    
    with open("user.json", "w") as f:
        f.write(json_data)
    print (user)
    
    with open("user.json", "r") as f:
        json_data = f.read()
    user=User.model_validate_json(json_data)
    print (user)