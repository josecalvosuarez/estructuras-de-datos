# user_profiles.py

import pickle

def save_profiles(profiles, filename="users.dat"):
    with open(filename, "wb") as f:
        pickle.dump(profiles, f)
    print("Profiles saved to binary file.")

def load_profiles(filename="users.dat"):
    try:
        with open(filename, "rb") as f:
            profiles = pickle.load(f)
            return profiles
    except FileNotFoundError:
        print("No profile file found.")
        return {}

# Example usage
if __name__ == "__main__":
    users = {
        "alice": {"age": 30, "email": "alice@example.com"},
        "bob": {"age": 24, "email": "bob@example.com"},
    }

    save_profiles(users)
    loaded_users = load_profiles()
    
    print("Loaded Profiles:")
    for username, info in loaded_users.items():
        print(f"{username} - Age: {info['age']}, Email: {info['email']}")
