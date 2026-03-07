import requests

url = "http://localhost:8000/api/v1/auth/register"
headers = {
    "Origin": "http://localhost:5173",
    "Access-Control-Request-Method": "POST",
}

try:
    response = requests.options(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Error: {e}")
