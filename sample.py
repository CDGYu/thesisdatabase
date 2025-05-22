import requests

url = "http://127.0.0.1:5000//create_user"

data = {
    "first_name": "Sample",
    "last_name": "Dela Cruz",
    "contact_number": "09123456789",
    "user_birthday": "1990-01-01",
    "password": "securepass1234",
    "email_address": "juan@example.com"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 201:
    data = response.json()
    print("User created:", response.json())
    user_id = data["User ID"]
    print(f"User ID: {user_id}")
else:
    print("Error:", response.status_code, response.text)

