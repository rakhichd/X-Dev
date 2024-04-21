import React, { useState } from "react"
import Button from "../Button/Button"
import getHighLow from "../../api/getHighLow";
import { useGlobalState, setGlobalState } from "../../state/state";

export default function StartHighLow({ setStart, setPosts }) {

    const [gameStarted, setGameStarted] = useState(false);

    const handleGame = async () => {
        setGameStarted(true);
        const { resultJson } = await getHighLow()
        console.log(resultJson)
        const tweetsArray = [];
        for (const user in resultJson) {
            const userTweets = resultJson[user];
            for (const tweetIndex in userTweets) {
                const tweet = userTweets[tweetIndex];
                tweetsArray.push({
                    user: user,
                    id: tweet.id,
                    text: tweet.text,
                    likes: tweet.metrics.like_count
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
                <div>
                    <Button className={"active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick={handleGame}>Start Game</Button>
                </div>
            ) : (
                <div>
                    <p>Game is starting...</p>
                </div>
            )}
        </div>
    );

}