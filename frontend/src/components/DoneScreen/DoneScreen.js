import React, { useState, useEffect }  from "react"
import Button from "../Button/Button"
import { FaRetweet } from "react-icons/fa6";

import interactTweet from "../../api/interactTweet";
import getTweets from "../../api/getTweets";
import { IoMdHeartEmpty } from "react-icons/io";
import { IoMdHeart } from "react-icons/io";




export default function DoneScreen({ tweetsByUser}) {

    const handleInteract = async (interact_type, tweet_id, author_id) => {
        
        const { resultJson } = await interactTweet(interact_type, tweet_id, author_id);
        
    };

    // const tweetsByUser = {
    //       "DevinBook": {
    //         "0": {
    //           "author_id": "237073728",
    //           "id": "1620863399466004483",
    //           "metrics": {
    //             "bookmark_count": 14,
    //             "impression_count": 1463455,
    //             "like_count": 8119,
    //             "quote_count": 159,
    //             "reply_count": 269,
    //             "retweet_count": 584
    //           },
    //           "text": "Roundin\u2019 3rd"
    //         },
    //         "1": {
    //           "author_id": "237073728",
    //           "id": "1613049011296161793",
    //           "metrics": {
    //             "bookmark_count": 80,
    //             "impression_count": 2144845,
    //             "like_count": 9155,
    //             "quote_count": 92,
    //             "reply_count": 277,
    //             "retweet_count": 557
    //           },
    //           "text": "What kinda question was that"
    //         },
    //         "2": {
    //           "author_id": "237073728",
    //           "id": "1618481636794068994",
    //           "metrics": {
    //             "bookmark_count": 35,
    //             "impression_count": 1519695,
    //             "like_count": 13233,
    //             "quote_count": 55,
    //             "reply_count": 163,
    //             "retweet_count": 658
    //           },
    //           "text": "Damn dame"
    //         },
    //         "3": {
    //           "author_id": "237073728",
    //           "id": "1611097669828759553",
    //           "metrics": {
    //             "bookmark_count": 502,
    //             "impression_count": 5789453,
    //             "like_count": 44436,
    //             "quote_count": 298,
    //             "reply_count": 340,
    //             "retweet_count": 5987
    //           },
    //           "text": "\u201cNobody cares\nGo to work\u201d-@KDTrey5"
    //         }
    //       },
    //       "KingJames": {
    //         "0": {
    //           "author_id": "23083404",
    //           "id": "1610123473786912768",
    //           "metrics": {
    //             "bookmark_count": 117,
    //             "impression_count": 8907248,
    //             "like_count": 87393,
    //             "quote_count": 310,
    //             "reply_count": 701,
    //             "retweet_count": 3496
    //           },
    //           "text": "\ud83d\udd77\ufe0f you're INSANE!!!!! \ud83d\udc4f\ud83c\udffe\ud83d\udc4f\ud83c\udffe\ud83d\udc4f\ud83c\udffe\ud83d\udc4f\ud83c\udffe"
    //         },
    //         "1": {
    //           "author_id": "23083404",
    //           "id": "1619143671303266304",
    //           "metrics": {
    //             "bookmark_count": 818,
    //             "impression_count": 27106812,
    //             "like_count": 130405,
    //             "quote_count": 5313,
    //             "reply_count": 5909,
    //             "retweet_count": 17368
    //           },
    //           "text": "WE ARE OUR OWN WORSE ENEMY!!!"
    //         },
    //         "2": {
    //           "author_id": "23083404",
    //           "id": "1619585191055618049",
    //           "metrics": {
    //             "bookmark_count": 635,
    //             "impression_count": 21630254,
    //             "like_count": 225245,
    //             "quote_count": 3657,
    //             "reply_count": 9293,
    //             "retweet_count": 17555
    //           },
    //           "text": "That one hurt BIG TIME!!! I don't understand"
    //         },
    //         "3": {
    //           "author_id": "23083404",
    //           "id": "1621628645721755650",
    //           "metrics": {
    //             "bookmark_count": 662,
    //             "impression_count": 33847713,
    //             "like_count": 249617,
    //             "quote_count": 13316,
    //             "reply_count": 7136,
    //             "retweet_count": 21552
    //           },
    //           "text": "\ud83d\udc40\ud83d\udc51"
    //         }
    //       },
    //       "StephenCurry30": {
    //         "0": {
    //           "author_id": "42562446",
    //           "id": "1617953991144648704",
    //           "metrics": {
    //             "bookmark_count": 0,
    //             "impression_count": 5234,
    //             "like_count": 35,
    //             "quote_count": 0,
    //             "reply_count": 16,
    //             "retweet_count": 2
    //           },
    //           "text": "@BostonSchools @tbaupdates @AthleticsBPS Buckets!!"
    //         },
    //         "1": {
    //           "author_id": "42562446",
    //           "id": "1620481491183742976",
    //           "metrics": {
    //             "bookmark_count": 0,
    //             "impression_count": 7994,
    //             "like_count": 46,
    //             "quote_count": 0,
    //             "reply_count": 23,
    //             "retweet_count": 2
    //           },
    //           "text": "@CABrownTV Love the moves!! \ud83d\ude02\ud83d\ude02"
    //         }
    //       },
    //       "profile_images": {
    //         "DevinBook": "https://pbs.twimg.com/profile_images/1709446587590885376/cM-UdR4k_normal.jpg",
    //         "KingJames": "https://pbs.twimg.com/profile_images/1759218232752304128/lEMgDMqr_normal.jpg",
    //         "StephenCurry30": "https://pbs.twimg.com/profile_images/1717296927522648064/nzm8Wp0A_normal.jpg",
    //         "stephenasmith": "https://pbs.twimg.com/profile_images/1724515058376400896/LM2zVPsV_normal.jpg"
    //       },
    //       "stephenasmith": {
    //         "0": {
    //           "author_id": "16302242",
    //           "id": "1612626364234084352",
    //           "metrics": {
    //             "bookmark_count": 23,
    //             "impression_count": 1551242,
    //             "like_count": 8558,
    //             "quote_count": 234,
    //             "reply_count": 896,
    //             "retweet_count": 658
    //           },
    //           "text": "See, this is what ticks me off. I knew @TCUFootball was the inferior team \u2014 but I went with the Cinderella pick. A loss is cool, especially to a powerhouse like @GeorgiaFootball. But to get your ass kicked shows me ya never belonged in the game to begin with.#Damn!"
    //         },
    //         "1": {
    //           "author_id": "16302242",
    //           "id": "1615812590680289280",
    //           "metrics": {
    //             "bookmark_count": 212,
    //             "impression_count": 6822499,
    //             "like_count": 11544,
    //             "quote_count": 405,
    //             "reply_count": 1867,
    //             "retweet_count": 343
    //           },
    //           "text": "Has been removed. My social management team will never make a mistake like this again. My apologies again to @Rihanna. And just to be clear, I\u2019m a huge fan. Sherri and I were just having fun. That is all."
    //         },
    //         "2": {
    //           "author_id": "16302242",
    //           "id": "1614480276381384706",
    //           "metrics": {
    //             "bookmark_count": 126,
    //             "impression_count": 3833824,
    //             "like_count": 35591,
    //             "quote_count": 668,
    //             "reply_count": 1446,
    //             "retweet_count": 4487
    //           },
    //           "text": "Congratulations @SeanPayton. Welcome to Los Angeles as the new coach is the @chargers. There is no way Brandon Staley can keep his job after blowing this lead. There\u2019s no coming back from this for him!"
    //         },
    //         "3": {
    //           "author_id": "16302242",
    //           "id": "1610117980913909762",
    //           "metrics": {
    //             "bookmark_count": 44,
    //             "impression_count": 2849379,
    //             "like_count": 48484,
    //             "quote_count": 54,
    //             "reply_count": 590,
    //             "retweet_count": 2352
    //           },
    //           "text": "Damn, this is scary. Prayers up for @BuffaloBills Safety Damar Hamlin \u2014 who\u2019s in critical condition. Just praying this brother survives and ends up okay.#\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe"
    //         }
    //       }
    //     }

    const [currentIndex, setCurrentIndex] = useState(0);

    const users = Object.keys(tweetsByUser).filter(key => key !== 'profile_images');

    const handlePrev = () => {
        console.log(currentIndex);
        setCurrentIndex((prevIndex) => {
            if (prevIndex === 0) return users.length-1;
            else return prevIndex-1;
        });
    };
    
    const handleNext = () => {
        console.log(currentIndex);
        setCurrentIndex((prevIndex) => {
            if (prevIndex === users.length-1) return 0;
            else return prevIndex+1;
        });
    };

    const [follows, setFollows] = useState({});
    const [likes, setLikes] = useState({});
    
      // Function to update a single key-value pair in the dictionary
      const updateFollows = (user, value) => {
        setFollows(prev => ({
          ...prev,  // Copy the previous dictionary
          [user]: value     // Update the specific key with the new value
        }));
      };

      const updateLikes = (id, value) => {
        setLikes(prev => ({
          ...prev,  // Copy the previous dictionary
          [id]: value     // Update the specific key with the new value
        }));
      };
    
    function userInitialize() {
        for (const user in tweetsByUser) {
            if (user === "profile_images") {
                continue;
            }
            updateFollows(user, 0);
            const userTweets = tweetsByUser[user];
            for (const tweetIndex in userTweets) {
                updateLikes(userTweets[tweetIndex].id, 0);
            }
    }}

    useEffect(() => {
        userInitialize();
        console.log(users);
        console.log(tweetsByUser);
    }, []);

    
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-4">
                <button onClick={handlePrev} className="text-gray-500 hover:bg-gray-100 rounded-full py-3 px-6">
                    Prev
                </button>
                <h2 className="text-2xl font-bold flex items-center">
                    <img 
                        src={tweetsByUser.profile_images[users[currentIndex]]}
                        alt={users[currentIndex]}
                        className = "rounded-full h-20 w-20 mr-5"
                    />
                    {users[currentIndex]} 
                        <div onClick={() => {
                            updateFollows(users[currentIndex], 1);
                            handleInteract(0, 0, tweetsByUser[users[currentIndex]][0].author_id);}}> 
                                <Button className="hover:bg-gray-800 border border-opacity-100 px-3 py-1 rounded-full border-black bg-black text-white text-sm ml-4">
                                    {follows[users[currentIndex]] === 1 ? 'Following' : 'Follow'}
                                </Button>
                        </div>
                    </h2>
                <button onClick={handleNext} className="text-gray-500 hover:bg-gray-100 rounded-full py-3 px-5">
                    Next
                </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.values(tweetsByUser[users[currentIndex]]).map((tweet, idx) => (
                    <div key={idx} className="bg-blue-100 p-4 rounded-lg shadow">
                        {tweet.author_id && (
                            <p className="font-semibold">{tweet.text}</p>
                        )}

                        <div className="flex items-end justify-center gap-3">
                            <Button onClick = {() => handleInteract(2, tweetsByUser[users[currentIndex]][idx].id, 0)} className="rounded-full p-1 hover:bg-green-100">
                                <FaRetweet />
                            </Button>
                            <p className="text-gray-500 text-sm mt-2 rounded-full p-1 hover:bg-transparent">@{users[currentIndex]}</p>
                            <div onClick={() => {
                                handleInteract(1, tweetsByUser[users[currentIndex]][idx].id, 0); 
                                updateLikes(tweetsByUser[users[currentIndex]][idx].id, 1)}}> 
                                <Button className="rounded-full p-1 hover:text-red-800">
                                    {likes[tweetsByUser[users[currentIndex]][idx].id] === 1 ? <IoMdHeart className="text-red-600" /> : <IoMdHeartEmpty />}
                                </Button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="mt-10 flex items-center justify-center">
                <div className="animate-pulse text-red-800 text-4xl font-extrabold">
                    Game Over.
                </div>
            </div>
        </div>
    );
}
