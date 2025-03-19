import requests

url = "http://127.0.0.1:8000/analyze"
headers = {"Content-Type": "application/json"}
data = {
    "text": "Patient reports neck pain after a car accident. Diagnosis: whiplash injury. Treatment: physiotherapy."
}

response = requests.post(url, json=data, headers=headers)
print(response.json())