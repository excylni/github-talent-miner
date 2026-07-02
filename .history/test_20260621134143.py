import requests
import os

os.getenv("GITHUB_TOKEN")
response = requests.get(
    "https://api.github.com/search/users",
    params={"q": "location:berlin", "per_page": 5},
    headers={"Authorization": f"token {GITHUB_TOKEN}"}
)
print(response.json())