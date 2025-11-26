import requests

try:
    response = requests.get('http://127.0.0.1:8000/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 500:
        with open('debug_500.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Saved 500 error page to debug_500.html")
except Exception as e:
    print(f"Error: {e}")
