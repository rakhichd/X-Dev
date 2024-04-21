import React, { useState } from "react"
import Button from "../Button/Button"
import getHighLow from "../../api/getHighLow";
import { useGlobalState, setGlobalState } from "../../state/state";

export default function StartHighLow({ setStart, setPosts }) {

    const [gameStarted, setGameStarted] = useState(false);

    const handleGame = async () => {
        setGameStarted(true);
        const { resultJson } = await getHighLow()
        const tweetsArray = [];
        console.log(resultJson)
        for (const user in resultJson) {
            if (user == "profile_image") {
                continue;
            }
            const userTweets = resultJson[user];
            for (const tweetIndex in userTweets) {
                const tweet = userTweets[tweetIndex];
                tweetsArray.push({
                    user: user,
                    author_id: tweet.author_id,
                    id: tweet.id,
                    text: tweet.text,
                    profile_image: resultJson.profile_image,
                    likes: tweet.metrics.like_count,
                });
            }
        }
        console.log(tweetsArray)
        setPosts(tweetsArray)
        setStart(true)
        setGameStarted(false)
    };

    return (
        <div className="container mx-auto px-4 py-8">
            {!gameStarted ? (
                <div className="w-[600px] flex flex-col items-center gap-8 mt-20">
                    <h1 className="text-xl text-center">Given two posts from the same person, guess which post has more likes! The game end when you get one wrong.</h1>
                    <Button className={"hover:bg-gray-200 duration-200 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick={handleGame}>Start Game</Button>
                </div>
            ) : (
                <div>
                    <p>Game is starting...</p>
                </div>
            )}
        </div>
    );

}