import os
import sys
import requests
from typing import List, Dict, Any
from pydantic import BaseModel, Field


# Ensuring our Data Type
class GitHubUser(BaseModel):
    id: int
    login: str
    html_url: str
    score: float
    type: str


# CLIENT ZONE 
class GitHubMiner:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            print("ERROR: GITHUB_TOKEN variable not found")
            sys.exit(1)

        self.base_url = "https://api.github.com/search/users"
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def fetch_developers_by_location(self, location: str, max_pages: int = 2) -> List[GitHubUser]:
        """Queries the GitHub API for users in a specific location
        """
        discovered_users = []
        query = f"location: {location}"

        for page in range(1, max_pages +1):
            params: Dict [str, Any] = {
                "q": query,
                "per_page": 50,
                "page": page
            }

            print(f"📡 Querying GitHub for {location} (Page {page})...")
            response = requests.get(self.base_url, headers=self.headers, params=params)

            if response.status_code != 200:
                print(f"API Error {response.status_code}: {response.text}")
                break

            data = response.json()
            items = data.get("items", [])

            if not items:
                print("No more users left for this query")
                break

            for item in items:
                #Enforcing the Pydantic type layout:
                try: 
                    user = GitHubUser(**item)
                    discovered_users.append(user)
                except Exception as e:
                    print(f"Skipped item because of {e}")
        
        return discovered_users

if __name__ == "__main__":
    miner = GitHubMiner()
    for city in ["Nuremberg", "Berlin"]:
        users = miner.fetch_developers_by_location(location=city, max_pages=1)
        print(f"Successfully fetched {len(users)} profiles inside {city}.\n")