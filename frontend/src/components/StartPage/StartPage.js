import React, { useState, useEffect } from "react";
import Button from "../Button/Button";
import getTweets from "../../api/getTweets";
import { FaUserFriends } from "react-icons/fa";
import { useGlobalState, setGlobalState } from "../../state/state";

export default function StartPage({
  setIncorrectTiles,
  shuffle,
  setStart,
  setFullArr,
}) {
  const [gameStarted, setGameStarted] = useState(false);
  const [people] = useGlobalState("people");
  const [startDate] = useGlobalState("startDate");

  const handleGame = async () => {
    setGameStarted(true);
    const { resultJson } = await getTweets(people, startDate);
    const tweetsArray = [];
    const fullArr = resultJson;

    for (const user in resultJson) {
      if (user == "profile_images") {
        continue;
      }
      const userTweets = resultJson[user];
      for (const tweetIndex in userTweets) {
        const tweet = userTweets[tweetIndex];
        tweetsArray.push({
          user: user,
          id: tweet.id,
          text: tweet.text,
        });
      }
    }
    setIncorrectTiles(shuffle(tweetsArray));
    setStart(false);
    setGameStarted(false);
    setFullArr(fullArr);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {!gameStarted ? (
        <div className="w-[600px] flex flex-col items-center gap-8 mt-20">
          <h1 className="text-center text-xl">
            Given four people, each with four posts, match posts that belong to
            the same person! The game ends when all posts are matched, or you lose
            your four lives.
          </h1>
          <div className="flex gap-3">
            <Button
              className={
                "hover:bg-gray-100 h-14 duration-200 border border-opacity-100 px-6 py-2 rounded-full border-black text-lg"
              }
              onClick={handleGame}
            >
              Start Game
            </Button>
            <CustomizeButton />
          </div>
        </div>
      ) : (
        <div className="mt-[200px]">
          <p>Game is starting...</p>
        </div>
      )}
    </div>
  );
}

