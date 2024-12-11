import requests
import json

# Set your API key here
api_key = "AIzaSyDML29qTmylzApq1J9zkhIzg4fEebY5zEU"

# Define the endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

# Define the payload
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works"
                }
            ]
        }
    ]
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Print the response (generated content)
if response.status_code == 200:
    response_data = response.json()
    print("Generated Response:", response_data)
else:
    print("Error:", response.status_code, response.text)
