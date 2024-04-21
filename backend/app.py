from flask import Flask, request, jsonify
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

CORS(app)
cors = CORS(app, supports_credentials=True, resource={
    r"/*":{
        "origins":"*"
    }
})

os.environ['XAI_API_KEY'] = 'Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ'

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAIShtQEAAAAAX5yH8Y5AT6WB5RtgNuNuqBJwY30%3DOqrBQEx2w81UOBuINmPO5bBb73jW1V44yMwkJ5JoqmzGR3fCwU",
                        consumer_key="wDcdhO9o75G5ZFsnMnFK16LTS",
                        consumer_secret="rsQf7GMYLORyXDaoYbHDigLvlMhdJRPDRE1A2MMsT1CjiD6Veb")

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
show_user_url = 'https://api.twitter.com/1.1/users/show.json'

# Routes
@app.route('/')
def nothing():
    return "empty route"

@app.route('/callback')
def callback():
    # Accept the callback params, get the token and call the API to
    # display the logged-in user's name and handle
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_denied = request.args.get('denied')


@app.route("/generate_game", methods=["POST"])
def generate_game():

    data = request.json
    custom_users = data.get('custom_users')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    # Default users
    users = ["elonmusk", "VancityReynolds", "KDTrey5", "NICKIMINAJ"]
    # Override with custom users
    if custom_users:
        users = custom_users

    results = {}

    # # Replace with time period of your choice
    # start_time = '2023-01-01T00:00:00Z'

    # # Replace with time period of your choice
    # end_time = '2023-08-01T00:00:00Z'

    for user in users:
        results[user] = getTopTweets(user, start_time, end_time)
    
    return jsonify(results), 200


def getTopTweets(username, start_time, end_time):

    def createTweetObjects(tweets):
        lst = []
        for tweet in tweets:
            lst.append(TweetObject(tweet))
        return lst
    
    query = f'from: {username} -is:retweet -has:links'

    time.sleep(0.8)
    tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at', 'public_metrics'],
                                  start_time=start_time,
                                  end_time=end_time, max_results=100)

    if tweets.data:
        tweetObjectLst = createTweetObjects(tweets.data)
    else:
        print("They do not tweet")
        return jsonify({"error": f"{username} does not have any tweets"}), 400

    min_heap = []

    for i, tweetObject in enumerate(tweetObjectLst):
        if i < 4:
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
            tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at', 'public_metrics'],
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
        dict[i] = tweet_dict
        i += 1
    return dict

@app.route("/hint", methods=["POST"])
async def hint():

    data = request.json
    hinted_user = data.get('hinted_user')

    client = xai_sdk.Client()
    sampler = client.sampler

    PREAMBLE = """\
    Human: I want you to share some fun facts about this person and these fun facts SHOULD NOT INCLUDE THE PERSON'S NAME.

    Please return a single sentence for the response, ending with a period.
    
    Please replace the person's name in the response with their pronouns instead. PLEASE DO NOT USE THE PERSON'S NAME WHEN WRITING THESE FUN FACTS. ONLY USE THE PERSON'S PRONOUNS. FOR EXAMPLE, DON'T USE THE NAME "KANYE WEST". INSTEAD REFER TO "KANYE WEST" WITH A PRONOUN LIKE "THEY".

    For eg. if the answer is "Donald Trump is the only president in U.S. history to have been impeached twice", your output should be "They are the only president in U.S. history to have been impeached twice".<|separator|>

    Assistant: Understood! Please provide the person's name."""

    prompt = PREAMBLE + f"<|separator|>\n\nHuman: {hinted_user}<|separator|>\n\nAssistant: "

    output = ""
    async for token in  sampler.sample(
        prompt=prompt,
        max_len=50,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.8):
        output += token.token_str
    
    output = output.split("\n")[0]

    return jsonify({"hint": output}), 200

@app.route("/generate_higherlower", methods=["POST"])
def generate_higherlower():
    usernames = ["elonmusk", "BarackObama", "katyperry", 
                 "taylorswift13", "kanyewest", "KimKardashian"]
    
    time_now = datetime.now()
    time_earlier = time_now - timedelta(days=30)
    start_time = time_earlier.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = time_now.strftime("%Y-%m-%dT%H:%M:%SZ")

    results = {}

    rand_user1 = usernames[random.randint(0, 6)]
    rand_user2 = usernames[random.randint(0, 6)]
    while rand_user1 == rand_user2:
        rand_user2 = usernames[random.randint(0, 6)]
    
    results[rand_user1] = getTopTweets(rand_user1, start_time, end_time)
    results[rand_user2] = getTopTweets(rand_user2, start_time, end_time)

    print(results)
    
    return jsonify(results), 200
    

class TweetObject:
    def __init__(self, tweet):
        self.text = tweet.text
        self.metrics = tweet.public_metrics
        self.id = tweet.id
        self.popularity = self.metrics["retweet_count"] + self.metrics["reply_count"] + self.metrics["like_count"]
    
    def __lt__(self, other):
        return self.popularity < other.popularity

if __name__ == "__main__":
    # app.run(debug=True)
    generate_game(None)