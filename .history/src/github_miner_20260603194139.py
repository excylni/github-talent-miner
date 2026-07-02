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


