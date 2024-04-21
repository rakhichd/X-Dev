import Button from "../Button/Button"
import React, { useState, useEffect } from "react"
import DoneScreen from "../DoneScreen/DoneScreen";
import StartPage from "../StartPage/StartPage.js";

export default function Main() {

    const [mistakesRemaining, setMistakesRemaining] = useState(4);
    const [selectedTiles, setSelectedTiles] = useState([]);
    const [tweets, setTweets] = useState([]);
    const [correctTiles, setCorrectTiles] = useState([]);
    const [incorrectTiles, setIncorrectTiles] = useState([]);
    const [done, setDone] = useState(false);
    const [oneAway, setOneAway] = useState(false);
    const [start, setStart] = useState(true);

    const tweetsByUser = {
          "DevinBook": {
            "0": {
              "author_id": 237073728,
              "id": 1620863399466004483,
              "metrics": {
                "bookmark_count": 14,
                "impression_count": 1463455,
                "like_count": 8119,
                "quote_count": 159,
                "reply_count": 269,
                "retweet_count": 584
              },
              "text": "Roundin\u2019 3rd"
            },
            "1": {
              "author_id": 237073728,
              "id": 1613049011296161793,
              "metrics": {
                "bookmark_count": 80,
                "impression_count": 2144845,
                "like_count": 9155,
                "quote_count": 92,
                "reply_count": 277,
                "retweet_count": 557
              },
              "text": "What kinda question was that"
            },
            "2": {
              "author_id": 237073728,
              "id": 1618481636794068994,
              "metrics": {
                "bookmark_count": 35,
                "impression_count": 1519695,
                "like_count": 13233,
                "quote_count": 55,
                "reply_count": 163,
                "retweet_count": 658
              },
              "text": "Damn dame"
            },
            "3": {
              "author_id": 237073728,
              "id": 1611097669828759553,
              "metrics": {
                "bookmark_count": 502,
                "impression_count": 5789453,
                "like_count": 44436,
                "quote_count": 298,
                "reply_count": 340,
                "retweet_count": 5987
              },
              "text": "\u201cNobody cares\nGo to work\u201d-@KDTrey5"
            }
          },
          "KingJames": {
            "0": {
              "author_id": 23083404,
              "id": 1610123473786912768,
              "metrics": {
                "bookmark_count": 117,
                "impression_count": 8907248,
                "like_count": 87393,
                "quote_count": 310,
                "reply_count": 701,
                "retweet_count": 3496
              },
              "text": "\ud83d\udd77\ufe0f you're INSANE!!!!! \ud83d\udc4f\ud83c\udffe\ud83d\udc4f\ud83c\udffe\ud83d\udc4f\ud83c\udffe\ud83d\udc4f\ud83c\udffe"
            },
            "1": {
              "author_id": 23083404,
              "id": 1619143671303266304,
              "metrics": {
                "bookmark_count": 818,
                "impression_count": 27106812,
                "like_count": 130405,
                "quote_count": 5313,
                "reply_count": 5909,
                "retweet_count": 17368
              },
              "text": "WE ARE OUR OWN WORSE ENEMY!!!"
            },
            "2": {
              "author_id": 23083404,
              "id": 1619585191055618049,
              "metrics": {
                "bookmark_count": 635,
                "impression_count": 21630254,
                "like_count": 225245,
                "quote_count": 3657,
                "reply_count": 9293,
                "retweet_count": 17555
              },
              "text": "That one hurt BIG TIME!!! I don't understand"
            },
            "3": {
              "author_id": 23083404,
              "id": 1621628645721755650,
              "metrics": {
                "bookmark_count": 662,
                "impression_count": 33847713,
                "like_count": 249617,
                "quote_count": 13316,
                "reply_count": 7136,
                "retweet_count": 21552
              },
              "text": "\ud83d\udc40\ud83d\udc51"
            }
          },
          "StephenCurry30": {
            "0": {
              "author_id": 42562446,
              "id": 1617953991144648704,
              "metrics": {
                "bookmark_count": 0,
                "impression_count": 5234,
                "like_count": 35,
                "quote_count": 0,
                "reply_count": 16,
                "retweet_count": 2
              },
              "text": "@BostonSchools @tbaupdates @AthleticsBPS Buckets!!"
            },
            "1": {
              "author_id": 42562446,
              "id": 1620481491183742976,
              "metrics": {
                "bookmark_count": 0,
                "impression_count": 7994,
                "like_count": 46,
                "quote_count": 0,
                "reply_count": 23,
                "retweet_count": 2
              },
              "text": "@CABrownTV Love the moves!! \ud83d\ude02\ud83d\ude02"
            }
          },
          "profile_images": {
            "DevinBook": "https://pbs.twimg.com/profile_images/1709446587590885376/cM-UdR4k_normal.jpg",
            "KingJames": "https://pbs.twimg.com/profile_images/1759218232752304128/lEMgDMqr_normal.jpg",
            "StephenCurry30": "https://pbs.twimg.com/profile_images/1717296927522648064/nzm8Wp0A_normal.jpg",
            "stephenasmith": "https://pbs.twimg.com/profile_images/1724515058376400896/LM2zVPsV_normal.jpg"
          },
          "stephenasmith": {
            "0": {
              "author_id": 16302242,
              "id": 1612626364234084352,
              "metrics": {
                "bookmark_count": 23,
                "impression_count": 1551242,
                "like_count": 8558,
                "quote_count": 234,
                "reply_count": 896,
                "retweet_count": 658
              },
              "text": "See, this is what ticks me off. I knew @TCUFootball was the inferior team \u2014 but I went with the Cinderella pick. A loss is cool, especially to a powerhouse like @GeorgiaFootball. But to get your ass kicked shows me ya never belonged in the game to begin with.#Damn!"
            },
            "1": {
              "author_id": 16302242,
              "id": 1615812590680289280,
              "metrics": {
                "bookmark_count": 212,
                "impression_count": 6822499,
                "like_count": 11544,
                "quote_count": 405,
                "reply_count": 1867,
                "retweet_count": 343
              },
              "text": "Has been removed. My social management team will never make a mistake like this again. My apologies again to @Rihanna. And just to be clear, I\u2019m a huge fan. Sherri and I were just having fun. That is all."
            },
            "2": {
              "author_id": 16302242,
              "id": 1614480276381384706,
              "metrics": {
                "bookmark_count": 126,
                "impression_count": 3833824,
                "like_count": 35591,
                "quote_count": 668,
                "reply_count": 1446,
                "retweet_count": 4487
              },
              "text": "Congratulations @SeanPayton. Welcome to Los Angeles as the new coach is the @chargers. There is no way Brandon Staley can keep his job after blowing this lead. There\u2019s no coming back from this for him!"
            },
            "3": {
              "author_id": 16302242,
              "id": 1610117980913909762,
              "metrics": {
                "bookmark_count": 44,
                "impression_count": 2849379,
                "like_count": 48484,
                "quote_count": 54,
                "reply_count": 590,
                "retweet_count": 2352
              },
              "text": "Damn, this is scary. Prayers up for @BuffaloBills Safety Damar Hamlin \u2014 who\u2019s in critical condition. Just praying this brother survives and ends up okay.#\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe"
            }
          }
        }

    const tweetsArray = [];

    for (const user in tweetsByUser) {
        if (user === "profile_images") {
            continue; // Skip over if the user is "profile_images"
        }
        const userTweets = tweetsByUser[user];
        for (const tweetId in userTweets) {
            const tweet = userTweets[tweetId];
            tweetsArray.push({
                user: user,
                id: tweet.id,
                text: tweet.text
            });
        }
    }

    console.log(tweetsArray);

    useEffect(() => {
        const tweetsArray = [];
        for (const user in tweetsByUser) {
            if (user === "profile_images") {
                continue; // Skip over if the user is "profile_images"
            }
            const userTweets = tweetsByUser[user];
            for (const tweetId in userTweets) {
                const tweet = userTweets[tweetId];
                tweetsArray.push({
                    user: user,
                    id: tweet.id,
                    text: tweet.text
                });
            }
        }
        setIncorrectTiles(shuffle(tweetsArray));
    }, [])

    useEffect(() => {
        let timer;
        if (oneAway) {
            timer = setTimeout(() => {
                setOneAway(false);
            }, 5000); // 20 seconds
        }

        return () => clearTimeout(timer);
    }, [oneAway]);

    function shuffle(array) {
        const shuffledArray = [...array];
        for (let i = shuffledArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
        }
        return shuffledArray;
    }
    

    const shuffleBoard = () => {
        setIncorrectTiles(prev => shuffle(prev));
    };

    function deselectAll() {
        return setSelectedTiles([]);
    }


    const selectTweetTile = (id) => {
        setSelectedTiles(prev => {
            if (prev.includes(id)) {
                return prev.filter(tileId => tileId !== id); // Remove the ID if it's already in the array
            } else if (prev.length < 4) {
                return [...prev, id]; // Add the ID if it's not in the array and the array length is less than 4
            }
            return prev; // Return the original array if it doesn't meet the conditions
        });
    };
    
    

    function MistakesRemaining() { // num of dots to show up based on how many mistakes are remaining 
        return (
            <div className="flex gap-1 items-center">
                {Array.from({ length: mistakesRemaining }).map((_, index) => (
                    <div key={index} className="rounded-full h-4 w-4 bg-gray-500"></div>
                ))}
            </div>
        );
    }

    function correctGuess() {
        const allGtiles = incorrectTiles.filter(tweet => selectedTiles.includes(tweet.id));
        const corr = correctTiles.concat(allGtiles);
        console.log(corr);
        setCorrectTiles(corr);
        const allStillWrong = incorrectTiles.filter(tweet => !corr.map(t => t.id).includes(tweet.id));
        setIncorrectTiles(allStillWrong);
        console.log(tweets);
        setSelectedTiles([]);
        if (allStillWrong.length === 0) {
            setDone(true);
        }
    }

    const handleStartGame = () => {
        setStart(false);
    };

    function submitGuesses() {
        const arrG = incorrectTiles.filter(tweet => selectedTiles.includes(tweet.id)); // based on selected tiles, get the user,id,text
        console.log(arrG);
        const users = arrG.map(tweet => tweet.user);
        if (arrG.length === 4) {
            if (users.every(user => user === users[0])) {
                correctGuess();
                console.log("true");
                return true; // All selected tweets have the same user
            } else {
                //deselectAll();
                // check if three users are all the same 
                users.sort();
                let countArr = 0;
                for (let i = 0; i < users.length-1; i++) {
                    if (users[i] === users[i+1]) {
                        countArr = countArr + 1;
                    }
                }
                if (countArr === 2) {
                    setOneAway(true);
                }
                console.log(countArr);
                setMistakesRemaining(mistakesRemaining -1);
                if (mistakesRemaining === 1) {
                    setDone(true);
                }
            }
        } 
        console.log("false");
        return false; // Selected tweets do not have the same user or not all tweets are selected
    }

    return (
        <div className="max-w-[100rem] ml-auto mr-auto">

            {!done ? (
                <>
                    {start ? (
                        <>
                           <StartPage handleStartGame = {handleStartGame}></StartPage>
                        </>
                    ) : (
                        <>
                             {oneAway && <div className = "fade-out mt-6">One Away...</div>}
                            <div className="grid gap-3 grid-cols-4 px-3 py-4 mt-7">
                                {correctTiles.slice(0, 4).map(tweet => (
                                    <Button
                                        key={tweet.id}
                                        className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-pink-100"
                                        onClick={() => selectTweetTile(tweet.id)}
                                    >
                                        {tweet.text}
                                    </Button>
                                ))}
                                {correctTiles.slice(4, 8).map(tweet => (
                                    <Button
                                        key={tweet.id}
                                        className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-green-100"
                                        onClick={() => selectTweetTile(tweet.id)}
                                    >
                                        {tweet.text}
                                    </Button>
                                ))}
                                {correctTiles.slice(8, 12).map(tweet => (
                                    <Button
                                        key={tweet.id}
                                        className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-yellow-100"
                                        onClick={() => selectTweetTile(tweet.id)}
                                    >
                                        {tweet.text}
                                    </Button>
                                ))}
                                {correctTiles.slice(12).map(tweet => (
                                    <Button
                                        key={tweet.id}
                                        className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-purple-100"
                                        onClick={() => selectTweetTile(tweet.id)}
                                    >
                                        {tweet.text}
                                    </Button>
                                ))}
                                    {incorrectTiles.map(tweet => (
                                        <Button
                                            key={tweet.id}
                                            className={`py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md ${selectedTiles.includes(tweet.id) ? "bg-blue-100" : "bg-gray-100"}`}
                                            onClick={() => selectTweetTile(tweet.id)}
                                        >
                                            {tweet.text}
                                        </Button>
                                    ))}
                                </div>

                            <div className="inline-block">
                                <div className="py-3 flex gap-2 "> <h1> Mistakes Remaining: </h1> <MistakesRemaining /> </div>
                            </div>

                            <div className="flex gap-2 place-content-center">
                                <Button className={"active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick={shuffleBoard}>Shuffle</Button>
                                <Button className={"active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick={deselectAll}>Deselect All</Button>
                                <Button className={"active:bg-blue-500 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick = {submitGuesses}>Submit</Button>
                                <Button className={"active:bg-blue-500 border border-opacity-100 px-6 py-2 rounded-full border-black"}>?</Button>
                            </div>
                        </>
                    )}
                </>
            ) : (
                <>
                    <DoneScreen></DoneScreen>
                </>
            )}
        </div>
    )
}