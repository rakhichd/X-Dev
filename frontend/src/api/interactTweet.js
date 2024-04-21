const interactTweet = async (interact_type, tweet_id, author_id) => {

  const result = await fetch("https://6b7f-8-25-197-34.ngrok-free.app/interact_tweet", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
        interact_type: interact_type,
        tweet_id: tweet_id,
        author_id: author_id
    }),
  });
  const resultJson = await result.json();
  const resultStatus = result.status;

  console.log(resultJson)

  return { resultJson, resultStatus };
};

export default interactTweet;
