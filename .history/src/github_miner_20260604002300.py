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

    def fetch_developers_by_location(self, location: str, max_pages: int = 2) -> List[GitHubUser]
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

            data = respond.json