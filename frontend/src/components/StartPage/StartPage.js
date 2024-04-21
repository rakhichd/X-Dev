import React, { useState, useEffect } from "react"
import Button from "../Button/Button"
import getTweets from "../../api/getTweets";
import { useGlobalState, setGlobalState } from "../../state/state";

export default function StartPage({ handleStartGame, setIncorrectTiles, shuffle, setStart }) {

    const [gameStarted, setGameStarted] = useState(false);
    const [people] = useGlobalState("people")

    const handleGame = async () => {
        setGameStarted(true);
        const { resultJson } = await getTweets([], 2020)
        const tweetsArray = [];
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
        setIncorrectTiles(shuffle(tweetsArray))
        setStart(false)
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