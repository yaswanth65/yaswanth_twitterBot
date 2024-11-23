from flask import Flask, render_template_string, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# Set your BEARER_TOKEN as an environment variable or replace with your actual token here
bearer_token =  "AAAAAAAAAAAAAAAAAAAAAGocwgEAAAAA%2BiEtspbVB6ntawvlDOGuI5KzF5A%3DoHla9Vz3RBgAQrw5vpZuesCUL8QwNEjpkdHc2dhRBHiaV5IzB5"

def create_url(ids):
    tweet_fields = "tweet.fields=lang,author_id"
    url = f"https://api.twitter.com/2/tweets?ids={ids}&{tweet_fields}"
    return url

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.get(url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    tweet_data = None
    error_message = None

    if request.method == 'POST':
        tweet_ids = request.form['tweet_ids']
        url = create_url(tweet_ids)
        try:
            tweet_data = connect_to_endpoint(url)
        except Exception as e:
            error_message = str(e)

    # HTML Template
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Twitter API - Tweet Lookup</title>
    </head>
    <body>
        <h1>Enter Tweet IDs to Lookup</h1>
        <form method="post">
            <label for="tweet_ids">Tweet IDs (comma-separated):</label>
            <input type="text" id="tweet_ids" name="tweet_ids" required>
            <button type="submit">Fetch Tweets</button>
        </form>

        {% if tweet_data %}
            <h2>Fetched Tweet Data:</h2>
            <pre>{{ tweet_data | tojson(indent=4) }}</pre>
        {% elif error_message %}
            <h2>Error:</h2>
            <pre>{{ error_message }}</pre>
        {% endif %}
    </body>
    </html>
    '''

    return render_template_string(html_template, tweet_data=tweet_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
