from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
import tweepy
import heapq
import time
import random
from datetime import datetime, timedelta
import os

import xai_sdk

import urllib.request
import oauth2 as oauth
import urllib.parse
import urllib.error

app = Flask(__name__)
app.secret_key = 'x_developer_challenge'

# CORS(app)
# cors = CORS(app, supports_credentials=True, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })

# CORS(app)
# CORS(app, supports_credentials=True)
# CORS(app, origins=['*'])  # Allows all origins

CORS(app)
cors = CORS(app, supports_credentials=True, resources={
    r"/*": {
    "origins": ["http://localhost:3000"]# Specify allowed origins explicitly
    }
})

os.environ['XAI_API_KEY'] = 'Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ'
os.environ['TWAUTH_APP_CONSUMER_KEY'] = 'wDcdhO9o75G5ZFsnMnFK16LTS'
os.environ['TWAUTH_APP_CONSUMER_SECRET'] = 'rsQf7GMYLORyXDaoYbHDigLvlMhdJRPDRE1A2MMsT1CjiD6Veb'

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['APP_CONSUMER_KEY'] = os.getenv('TWAUTH_APP_CONSUMER_KEY', 'API_Key_from_Twitter')
app.config['APP_CONSUMER_SECRET'] = os.getenv('TWAUTH_APP_CONSUMER_SECRET', 'API_Secret_from_Twitter')

oauth_store = {}

# client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAIShtQEAAAAAX5yH8Y5AT6WB5RtgNuNuqBJwY30%3DOqrBQEx2w81UOBuINmPO5bBb73jW1V44yMwkJ5JoqmzGR3fCwU",
#                         consumer_key="wDcdhO9o75G5ZFsnMnFK16LTS",
#                         consumer_secret="rsQf7GMYLORyXDaoYbHDigLvlMhdJRPDRE1A2MMsT1CjiD6Veb")

bearer_token="AAAAAAAAAAAAAAAAAAAAAIShtQEAAAAAX5yH8Y5AT6WB5RtgNuNuqBJwY30%3DOqrBQEx2w81UOBuINmPO5bBb73jW1V44yMwkJ5JoqmzGR3fCwU",
consumer_key="wDcdhO9o75G5ZFsnMnFK16LTS",
consumer_secret="rsQf7GMYLORyXDaoYbHDigLvlMhdJRPDRE1A2MMsT1CjiD6Veb"

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
show_user_url = 'https://api.twitter.com/1.1/users/show.json'
app_callback_url = 'https://444e-8-25-197-34.ngrok-free.app/callback' # Hardcoded to backend server

datetime_format = "%Y-%m-%dT%H:%M:%SZ"

def get_client():
    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAIShtQEAAAAAX5yH8Y5AT6WB5RtgNuNuqBJwY30%3DOqrBQEx2w81UOBuINmPO5bBb73jW1V44yMwkJ5JoqmzGR3fCwU",
                        consumer_key="wDcdhO9o75G5ZFsnMnFK16LTS",
                        consumer_secret="rsQf7GMYLORyXDaoYbHDigLvlMhdJRPDRE1A2MMsT1CjiD6Veb",
                        access_token=session["access_token"],
                        access_token_secret=session["access_token_secret"])
    return client

# Not used
@app.route('/')
def hello():

    consumer = oauth.Consumer(app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'])
    api = oauth.Client(consumer)
    
    resp, content = api.request(request_token_url, "POST", body=urllib.parse.urlencode({
                                   "oauth_callback": app_callback_url}))
    
    if resp['status'] != '200':
        error_message = 'Invalid response, status {status}, {message}'.format(
            status=resp['status'], message=content.decode('utf-8'))
        return jsonify({'error_message': error_message}, resp['status'])

    request_token = dict(urllib.parse.parse_qsl(content))
    oauth_token = request_token[b'oauth_token'].decode('utf-8')
    oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

    oauth_store[oauth_token] = oauth_token_secret

    return redirect(f"{authorize_url}?oauth_token={oauth_token}")

# Verify if user is logged in
@app.route('/verify')
def verify():
    if "screen_name" not in session:
        redirect('http://localhost:3000/')
    else:
        return jsonify({"screen_name": session["screen_name"]}, 200)

@app.route('/authenticate')
def authenticate():

    consumer = oauth.Consumer(app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'])
    api = oauth.Client(consumer)
    
    resp, content = api.request(request_token_url, "POST", body=urllib.parse.urlencode({
                                   "oauth_callback": app_callback_url}))
    
    if resp['status'] != '200':
        error_message = 'Invalid response, status {status}, {message}'.format(
            status=resp['status'], message=content.decode('utf-8'))
        return jsonify({'error_message': error_message}, resp['status'])

    request_token = dict(urllib.parse.parse_qsl(content))
    oauth_token = request_token[b'oauth_token'].decode('utf-8')
    oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

    oauth_store[oauth_token] = oauth_token_secret

    return jsonify({"link": f"{authorize_url}?oauth_token={oauth_token}"}, 200)

@app.route('/callback')
def callback():
    # Accept the callback params, get the token and call the API to
    # display the logged-in user's name and handle

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_denied = request.args.get('denied')

    # if the OAuth request was denied, delete our local token
    # and show an error message
    if oauth_denied:
        if oauth_denied in oauth_store:
            del oauth_store[oauth_denied]
        return jsonify({'error_message': "the OAuth request was denied by this user"}, 400)
    
    if not oauth_token or not oauth_verifier:
        return jsonify({'error_message': "callback param(s) missing"}, 400)

    # unless oauth_token is still stored locally, return error
    if oauth_token not in oauth_store:
        return jsonify({'error_message': "oauth_token not found locally"}, 400)
    
    oauth_token_secret = oauth_store[oauth_token]
    oauth_token_secret = oauth_store[oauth_token]

    consumer = oauth.Consumer(app.config['APP_CONSUMER_KEY'], app.config['APP_CONSUMER_SECRET'])
    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    api = oauth.Client(consumer, token)

    resp, content = api.request(access_token_url, "POST")
    access_token = dict(urllib.parse.parse_qsl(content))

    session["screen_name"] = access_token[b'screen_name'].decode('utf-8')
    session["user_id"] = access_token[b'user_id'].decode('utf-8')

    # These are the tokens you would store long term, someplace safe
    session["access_token"] = access_token[b'oauth_token'].decode('utf-8')
    session["access_token_secret"] = access_token[b'oauth_token_secret'].decode('utf-8')
    
    # don't keep this token and secret in memory any longer
    del oauth_store[oauth_token]
    
    return redirect('http://localhost:3000/whosaidthat')

@app.route("/generate_game", methods=["POST"])
def generate_game():

    data = request.json
    custom_users = data.get('custom_users')
    start_time = data.get('start_time')
    end_time = data.get('end_time') # end_time can be optionally none
    
    # Default users
    default_users = ["ChipotleTweets", "chrissyteigen", "elonmusk", "VancityReynolds", "NICKIMINAJ", "BarackObama", "neiltyson", "mcuban", "BernieSanders", "lexfridman", "MrBeast", "KingJames"]

    # Generate random users
    rand_user1 = default_users[random.randint(0, 11)]

    rand_user2 = default_users[random.randint(0, 11)]
    while rand_user2 == rand_user1:
        rand_user2 = default_users[random.randint(0, 11)]

    rand_user3 = default_users[random.randint(0, 11)]
    while rand_user3 == rand_user2 or rand_user3 == rand_user1:
        rand_user3 = default_users[random.randint(0, 11)]

    rand_user4 = default_users[random.randint(0, 11)]
    while rand_user4 == rand_user3 or rand_user4 == rand_user2 or rand_user4 == rand_user1:
        rand_user4 = default_users[random.randint(0, 11)]

    users = [rand_user1, rand_user2, rand_user3, rand_user4]


    # Override with custom users
    if custom_users:
        users = custom_users

    results = {}

    # if not end_time:
    start_datetime = datetime.strptime(start_time, datetime_format)
    end_datetime = start_datetime + timedelta(weeks=15) ## Hardcoded, change this
    end_time = end_datetime.strftime(datetime_format)

    results["profile_images"] = {}
    for user in users:
        results[user] = getTopTweets(user, start_time, end_time, 4)
        
        # Get profile image of user
        client = get_client()
        user_info = client.get_user(username=user, user_fields=['profile_image_url'])
        results["profile_images"][user] = user_info.data['profile_image_url']
    
    return jsonify(results), 200


def getTopTweets(username, start_time, end_time, num_tweets):
    def createTweetObjects(tweets):
        lst = []
        for tweet in tweets:
            lst.append(TweetObject(tweet))
        return lst
        
    query = f'from: {username} -is:retweet -has:links'

    time.sleep(0.8)
    client = get_client()
    tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at', 'public_metrics', 'author_id'],
                                  start_time=start_time,
                                  end_time=end_time, max_results=100)

    if tweets.data:
        tweetObjectLst = createTweetObjects(tweets.data)
    else:
        print("They do not tweet")
        return jsonify({"error": f"{username} does not have any tweets"}), 400

    min_heap = []

    for i, tweetObject in enumerate(tweetObjectLst):
        if i < num_tweets:
            heapq.heappush(min_heap, tweetObject)
        else:
            heapq.heappush(min_heap, tweetObject)
            heapq.heappop(min_heap)

    next_token = None
    if "next_token" in tweets.meta:
        next_token = tweets.meta["next_token"]

    while next_token:
        try: 
            time.sleep(0.8)
            tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at', 'public_metrics', 'author_id'],
                                        start_time=start_time,
                                        end_time=end_time, next_token=next_token, max_results=100)
            tweetObjectLst = createTweetObjects(tweets.data)

            for tweetObject in tweetObjectLst:
                heapq.heappush(min_heap, tweetObject)
                heapq.heappop(min_heap)
            
            if "next_token" in tweets.meta:
                next_token = tweets.meta["next_token"]
            else:
                break

        except tweepy.errors.TooManyRequests:
            print("Too many requests")
            break
    

    dict = {}
    i = 0
    while len(min_heap) > 0:
        tweet_dict = {}
        obj = heapq.heappop(min_heap)
        tweet_dict["id"] = obj.id
        tweet_dict["metrics"] = obj.metrics
        tweet_dict["text"] = obj.text
        tweet_dict["author_id"] = obj.author_id
        dict[i] = tweet_dict
        i += 1
    return dict

@app.route("/hint", methods=["POST"])
async def hint():

    data = request.json
    hinted_user = data.get('hinted_user')

    api = xai_sdk.Client()
    sampler = api.sampler

    PREAMBLE = """\
    Human: I want you to share some fun facts about this person and these fun facts SHOULD NOT INCLUDE THE PERSON'S NAME.

    Please return a single sentence for the response, ending with a period.
    
    Please replace the person's name in the response with their pronouns instead. PLEASE DO NOT USE THE PERSON'S NAME WHEN WRITING THESE FUN FACTS. ONLY USE THE PERSON'S PRONOUNS. FOR EXAMPLE, DON'T USE THE NAME "KANYE WEST". INSTEAD REFER TO "KANYE WEST" WITH A PRONOUN LIKE "THEY".

    For eg. if the answer is "Donald Trump is the only president in U.S. history to have been impeached twice", your output should be "They are the only president in U.S. history to have been impeached twice".<|separator|>

    Assistant: Understood! Please provide the person's name."""

    prompt = PREAMBLE + f"<|separator|>\n\nHuman: {hinted_user}<|separator|>\n\nAssistant: "

    output = ""
    async for token in sampler.sample(
        prompt=prompt,
        max_len=50,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.8):
        output += token.token_str
    
    output = output.split("\n")[0]

    return jsonify({"hint": output}), 200

@app.route("/interact_tweet", methods=["POST"])
def interact_tweet():

    data = request.json
    interact_type = data.get('interact_type')
    tweet_id = data.get('tweet_id')
    author_id = data.get('author_id')
    assert interact_type in [0, 1, 2] # 0: following, 1: like, 2: retweet

    client = get_client()
    if interact_type == 0:
        client.follow_user(target_user_id=author_id, user_auth=True)
    elif interact_type == 1:
        client.like(tweet_id=tweet_id, user_auth=True)
    else:
        client.retweet(tweet_id=tweet_id, user_auth=True)
    
    return jsonify({"message": "Successfully interacted with tweet"}, 200)

# Not used
@app.route("/generate_higherlower", methods=["POST"])
def generate_higherlower():
    usernames = ["elonmusk", "BarackObama", "BernieSanders", "mcuban", "lexfridman", "MrBeast", "KingJames"]
    
    # Get top 8 tweets within the year for a particular celebrity
    time_now = datetime.now()
    time_earlier = time_now - timedelta(weeks=13)
    start_time = time_earlier.strftime(datetime_format)
    end_time = time_now.strftime(datetime_format)

    results = {}

    rand_user = usernames[random.randint(0, 6)]
    results[rand_user] = getTopTweets(rand_user, start_time, end_time, 8)

    client = get_client()
    user_info = client.get_user(username=rand_user, user_fields=['profile_image_url'])
    results["profile_image"] = user_info.data['profile_image_url']
    
    return jsonify(results), 200
    

class TweetObject:
    def __init__(self, tweet):
        self.text = tweet.text
        self.metrics = tweet.public_metrics
        self.id = str(tweet.id)
        self.author_id = str(tweet.author_id)
        self.popularity = self.metrics["retweet_count"] + self.metrics["reply_count"] + self.metrics["like_count"]

    def __lt__(self, other):
        return self.popularity < other.popularity

if __name__ == "__main__":
    app.run(debug=True)