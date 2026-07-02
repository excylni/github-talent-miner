from src.github_miner import GitHubUser
import pytest 
from pydantic import ValidationError

def test_github_user_schema():
    """ TEST if our pydantic model correctly handles the data"""

    fake_api_response = {
        "id" : 9999
        "login" =
    }