import json

if __name__ == "__main__":
    data = {"jmeno": "Jan",
            "prijmeni": "Novak",
            "vek": 30,}
    json_data = json.dumps(data)
    print(json_data)
    with open("data.json", "w") as f:
        f.write(json_data)
    
    with open("data.json", "r") as f:
        json_data = f.read()
