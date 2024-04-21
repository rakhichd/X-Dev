from flask import Flask, request, jsonify
from flask_cors import CORS
import tweepy
import heapq
import time
from datetime import datetime

import xai_sdk

app = Flask(__name__)

CORS(app)
cors = CORS(app, supports_credentials=True, resource={
    r"/*":{
        "origins":"*"
    }
})

# Routes
@app.route('/')
def nothing():
    return "empty route"


@app.route("/generate_game", methods=["POST"])
def generate_game(request):

    data = request.json
    custom_users = data.get('custom_users')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAIShtQEAAAAAX5yH8Y5AT6WB5RtgNuNuqBJwY30%3DOqrBQEx2w81UOBuINmPO5bBb73jW1V44yMwkJ5JoqmzGR3fCwU",
                           consumer_key="wDcdhO9o75G5ZFsnMnFK16LTS",
                           consumer_secret="rsQf7GMYLORyXDaoYbHDigLvlMhdJRPDRE1A2MMsT1CjiD6Veb")
    
    # Default users
    users = ["elonmusk", "VancityReynolds", "KDTrey5", "NICKIMINAJ"]
    # Override with custom users
    if custom_users:
        users = custom_users

    results = {}

    # Replace with time period of your choice
    start_time = '2023-01-01T00:00:00Z'

    # Replace with time period of your choice
    end_time = '2023-08-01T00:00:00Z'

    for user in users:
        results[user] = getTopTweets(user, client, start_time, end_time)
    
    for user, tweetObjectList in results.items():
        print(user)
        for tweet in tweetObjectList:
            print(tweet)
        print("\n")
    
    return jsonify(results), 200


def getTopTweets(username, client, start_time, end_time):

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
        raise Exception(f"{username} does not have any tweets")

    min_heap = []

    for i, tweetObject in enumerate(tweetObjectLst):
        if i < 4:
            heapq.heappush(min_heap, tweetObject)
        else:
            heapq.heappush(min_heap, tweetObject)
            heapq.heappop(min_heap)

    next_token = tweets.meta["next_token"]

    num_requests = 0
    while next_token and num_requests < 10:
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
            print("Too many requests, index:" + str(num_requests))
            break

        num_requests += 1
    

    lst = []
    for i in range(4):
        lst.append(heapq.heappop(min_heap).tweet)
    return lst

@app.route("/hint", methods=["POST"])
async def hint(request):

    data = request.json
    hinted_user = data.get('hinted_user')

    client = xai_sdk.Client()
    prompt = f"Human: Give me a one sentence fun fact about {hinted_user} without mentioning their name."

    output = ""
    async for token in client.sampler.sample(prompt, max_len=50):
        output += token.token_str

    #Remove last incomplete sentence
    tokens = output.split("\n")
    proper_output = None
    for token in tokens:
        if not token == '':
            proper_output = token
    proper_output = proper_output.replace("Assistant: ", "")
    return jsonify({"hint": proper_output}), 200


class TweetObject:
    def __init__(self, tweet):
        self.tweet = tweet
        metrics = tweet.public_metrics
        self.popularity = metrics["retweet_count"] + metrics["reply_count"] + metrics["like_count"]
    
    def __lt__(self, other):
        return self.popularity < other.popularity

if __name__ == "__main__":
    # app.run(debug=True)
    generate_game(None)