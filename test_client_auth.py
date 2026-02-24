import requests

BASE_URL = "http://localhost:5000"


def register_user():
    print("Sending in john_doe as username, and ValidPassword1! as password.")
    data = {"username": "john_doe", "password": "ValidPassword1!"}
    response = requests.post(BASE_URL + "/register", json=data)
    print("REGISTER:", response.status_code, response.json())


def login_user():
    print("Sending in john_doe as username, and ValidPassword1! as password.")
    data = {"username": "john_doe", "password": "ValidPassword1!"}
    response = requests.post(BASE_URL + "/login", json=data)
    print("LOGIN:", response.status_code, response.json())


if __name__ == "__main__":
    register_user()
    login_user()