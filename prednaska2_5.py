import json
import pickle


if __name__ == "__main__":
    data = {"jmeno": "Jan",
            "prijmeni": "Novak",
            "vek": 30,}
    json_data = json.dumps(data)
    print(json_data)

    pickle_data = pickle.dumps(data)
    print(pickle_data)