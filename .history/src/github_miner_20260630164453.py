import os
import sys
import json
import requests
from typing import List, Dict, Any, Optional
import pandas as pd
from pydantic import BaseModel, ValidationError
from datetime import date


# Ensuring our Data Type
class GitHubUser(BaseModel):
    id: int
    login: str
    html_url: str
    score: float
    type: str

    company: Optional[str] = None
    location: Optional[str] = None
    followers: Optional[int] = None
    public_repos: Optional[int] = None
    bio: Optional[str] = None

# ----------------
# MINING ENGINE
# ----------------
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

    def fetch_developers_by_location(self, location: str, max_pages: int) -> tuple[list[dict],list[GitHubUser]]:
        """Queries the GitHub API for users in a specific location
        returns JSON and pydantic file
        """
        raw_data = []
        validated_data = []
        query = f"location:{location}"

        for page in range(1, max_pages +1):
            params: Dict [str, Any] = {
                "q": query,
                "per_page": 50,
                "page": page
            }

            print(f"Querying GitHub for {location} (Page {page})...")
            response = requests.get(self.base_url, headers=self.headers, params=params)

            if response.status_code != 200:
                print(f"API Error {response.status_code}: {response.text}")
                break

            data_raw = response.json()
            items = data_raw.get("items", [])

            if not items:
                print("No more users left for this query")
                break

            for item in items:
                # saving raw jsons
                raw_data.append(item)
                # Enforcing the Pydantic type layout:
                try: 
                    user = GitHubUser(**item)
                    validated_data.append(user)
                except Exception as e:
                    print(f"Skipped item because of {e}")
                    continue 
        return raw_data, validated_data

    def enrich_with_profile(self, item: dict) -> dict:
        """Calls the user profile to fetch company/location etc
        and merges those fields into a the dictionary."""
        resp = requests.get(
            
        )

# --------------
# STORAGE
# --------------

def saving_data(city: str, raw_data: list[dict], validated_data: list[GitHubUser]):
    """Saves raw data to JSON and validated to Apache Parquet"""
    today_str = date.today().isoformat()

    # Saving raw data
    if not raw_data:
        print(f"No data to save for city {city}")

    raw_path = f"data/raw/{today_str}_{city.lower()}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=4)
        print(f"Saved Json to {raw_path}")
    
    # Saving processed data
    processed_path = f"data/processed/{today_str}_{city.lower()}.parquet"
    # Convert into dictionary for Pandas
    records = [user.model_dump() for user in validated_data]

    df = pd.DataFrame(records)
    df.to_parquet(processed_path, index=False, compression="snappy")
    print(f"Optimized Parquet saved to: {processed_path}")
    



if __name__ == "__main__":
    miner = GitHubMiner()
    for city in ["Nuremberg", "Berlin"]:
        raw_data, validated_data = miner.fetch_developers_by_location(location=city, max_pages=15)
        print(f"Successfully fetched {len(validated_data)} profiles inside {city}.\n")
        saving_data(city, raw_data, validated_data)