from flask import Flask, request, render_template_string, redirect, url_for
from requests_oauthlib import OAuth1Session
import json

app = Flask(__name__)

# Twitter API credentials
consumer_key = "zb3p1WG7VTaxV2wRZl5ibqQwk"
consumer_secret = "NJQORRWOLW4oApfYtdQ6Y75BELXqTT95TOtUVUxM84oiA7YXmC"

# Placeholder for OAuth tokens
oauth_tokens = {}

@app.route('/')
def index():
    return '''
    <h1>Twitter OAuth Authorization</h1>
    <form action="/authorize" method="post">
        <button type="submit">Authorize and Tweet</button>
    </form>
    '''

@app.route('/authorize', methods=['POST'])
def authorize():
    # Step 1: Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        return "Error: There may be an issue with the consumer_key or consumer_secret you entered."

    # Store tokens for later use
    oauth_tokens['resource_owner_key'] = fetch_response.get("oauth_token")
    oauth_tokens['resource_owner_secret'] = fetch_response.get("oauth_token_secret")

    # Step 2: Get authorization URL
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)

    return f'''
    <p>Please <a href="{authorization_url}" target="_blank">authorize the app</a> and then enter the PIN below:</p>
    <form action="/post_tweet" method="post">
        <label for="pin">PIN:</label>
        <input type="text" id="pin" name="pin" required>
        <button type="submit">Submit PIN and Post Tweet</button>
    </form>
    '''

@app.route('/post_tweet', methods=['POST'])
def post_tweet():
    # Retrieve the verifier PIN from the user input
    verifier = request.form.get('pin')

    # Step 3: Exchange the request token for an access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_tokens['resource_owner_key'],
        resource_owner_secret=oauth_tokens['resource_owner_secret'],
        verifier=verifier,
    )

    oauth_tokens_response = oauth.fetch_access_token(access_token_url)
    access_token = oauth_tokens_response["oauth_token"]
    access_token_secret = oauth_tokens_response["oauth_token_secret"]

    # Step 4: Use the access tokens to post a tweet
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Define the payload with the tweet text
    payload = {"text": "Hellooo SE proj from the Flask app!"}
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

    if response.status_code != 201:
        return f"Error posting tweet: {response.status_code} {response.text}"

    json_response = response.json()
    return f"<h2>Tweet posted successfully!</h2><pre>{json.dumps(json_response, indent=4)}</pre>"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
