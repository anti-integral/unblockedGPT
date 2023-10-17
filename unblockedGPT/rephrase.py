import requests
from unblockedGPT.auth import Database
from unblockedGPT.GPTHeroAuth import gptHeroAuthLogin
# Define the base URL of your FastAPI-based API


def rephrase_2(essay: str) -> dict:
    """
        This function rephrases the result using the 2nd rephasing API.
        returns a dictionary with status bool and msg str
    """
    base_url = "https://gpthero.dev/api/"

    # Define the request payload
    auth = Database.get_instance()
    hero = gptHeroAuthLogin(auth.get_settings(2), auth.get_settings(3))
    if hero == False:
        return {'status':False, 'msg':"Sign in to GPT Hero"}
    request_payload = {
        "prompt": {
            "essay": essay,
            "approach": "Creative",
            "context": True,
            "randomness": 6,
            "tone": "informative",
            "difficulty": "easy to understand, very common vocabulary",
            "additional_adjectives": "concise and precise, to the point",
            "model": "GPT-3",
        },
        "user": {
            "auth_token": hero
        },
    }

    # Send a POST request to the /rephrase_essay endpoint
    response = requests.post(f"{base_url}/rephrase_essay", json=request_payload)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        rephrased_essay = response.json()
        rephrased_essay = rephrased_essay['rephrased_essay']
        return {'status':True, 'msg':rephrased_essay}
    elif response.status_code == 401:
        # Invalid API key
        return {'status':False, 'msg':"Invalid API key"}
        
    else:
        # Request failed
        error_message = response.json()

        return {'status':False, 'msg':f"Failed to rephrase essay\n {error_message['detail'][0]['msg']}"}

if __name__ == "__main__":
    essay = "Tz."
    print(rephrase_2(essay))
