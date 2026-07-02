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
        discovered_users