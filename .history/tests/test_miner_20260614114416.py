from src.github_miner import GitHubUser
import pytest 
from pydantic import ValidationError

def test_github_user_schema():
    """ TEST if our pydantic model correctly handles the data"""

    fake_api_response = {
        "id" : 9999,
        "login" : "test_developer",
        "html_url": "https://github.com/test_developer",
        "score": 1.0,
        "type": "User",
    }

    #Feed that data into Pydantic blueprint
    user = GitHubUser(**fake_api_response)

    # Verify 
    assert user.id == 9999
    assert user.login == "test_developer"

def test_github_user_schema_invalid():
    """TEST if our pydantic model handles wrong data"""

    fake_api_response = {
        "id" : "broken_test_id", #should be an integer
        "login" : "test_developer",
        "html_url": "https://github.com/test_developer",
        "score": 1.0,
        "type": "User",
    }

    with pytest.raises(ValidationError)