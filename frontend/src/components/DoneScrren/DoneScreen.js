import React, { useState, useEffect }  from "react"
import Button from "../Button/Button"
import { FaRetweet } from "react-icons/fa6";
import { IoMdHeartEmpty } from "react-icons/io";



export default function DoneScreen({status}) {

    const tweetsByUser = {
        "DevinBook": {
            "0": {
                "id": 1634000060190195712,
                "metrics": {
                    "bookmark_count": 291,
                    "impression_count": 3251945,
                    "like_count": 22241,
                    "quote_count": 409,
                    "reply_count": 661,
                    "retweet_count": 3294
                },
                "text": "cant fake humble just \u2018cause\nyour azz is insecure"
            },
            "1": {
                "id": 1658313833235222529,
                "metrics": {
                    "bookmark_count": 235,
                    "impression_count": 18693766,
                    "like_count": 30093,
                    "quote_count": 1151,
                    "reply_count": 1376,
                    "retweet_count": 3252
                },
                "text": "36 unbothered"
            },
            "2": {
                "id": 1611097669828759553,
                "metrics": {
                    "bookmark_count": 502,
                    "impression_count": 5789395,
                    "like_count": 44438,
                    "quote_count": 298,
                    "reply_count": 340,
                    "retweet_count": 5988
                },
                "text": "\u201cNobody cares\nGo to work\u201d-@KDTrey5"
            },
            "3": {
                "id": 1624586154493497344,
                "metrics": {
                    "bookmark_count": 556,
                    "impression_count": 10236767,
                    "like_count": 85200,
                    "quote_count": 2333,
                    "reply_count": 2375,
                    "retweet_count": 9727
                },
                "text": "Can all y\u2019all get out my city\nI like it better quiet"
            }
        },
        "KingJames": {
            "0": {
                "id": 1641836984195743749,
                "metrics": {
                    "bookmark_count": 2012,
                    "impression_count": 81951063,
                    "like_count": 254363,
                    "quote_count": 12029,
                    "reply_count": 13926,
                    "retweet_count": 19134
                },
                "text": "Welp guess my blue \u2714\ufe0f will be gone soon cause if you know me I ain\u2019t paying the 5. \ud83e\udd37\ud83c\udffe\u200d\u2642\ufe0f"
            },
            "1": {
                "id": 1684594877429092352,
                "metrics": {
                    "bookmark_count": 1291,
                    "impression_count": 21049416,
                    "like_count": 375993,
                    "quote_count": 2639,
                    "reply_count": 10458,
                    "retweet_count": 26901
                },
                "text": "I want to thank the countless people sending my family love and prayers. We feel you and I\u2019m so grateful. Everyone doing great. We have our family together, safe and healthy, and we feel your love. Will have more to say when we\u2019re ready but I wanted to tell everyone how much your\u2026 https://t.co/S2SAY48Gst"
            },
            "2": {
                "id": 1652365949629263872,
                "metrics": {
                    "bookmark_count": 4612,
                    "impression_count": 50613682,
                    "like_count": 381564,
                    "quote_count": 21927,
                    "reply_count": 15585,
                    "retweet_count": 55445
                },
                "text": "Unlike you little \ud83e\udd2cI'm a grown ass man\nBig shoes to fill \ud83e\udd2c, grown ass pants \nProlly hustled with your pops, go ask your parents \nIts apparent you're staring at a legend \nWho, put a few little \ud83e\udd2cin the they place before \nTrying to eat without saying they grace before! \ud83e\udd2b\ud83d\udc51"
            },
            "3": {
                "id": 1622394143912919041,
                "metrics": {
                    "bookmark_count": 11527,
                    "impression_count": 145609536,
                    "like_count": 451905,
                    "quote_count": 34593,
                    "reply_count": 20228,
                    "retweet_count": 70440
                },
                "text": "Maybe It\u2019s Me"
            }
        },
        "StephenCurry30": {
            "0": {
                "id": 1632470323886198785,
                "metrics": {
                    "bookmark_count": 57,
                    "impression_count": 1336153,
                    "like_count": 23995,
                    "quote_count": 800,
                    "reply_count": 686,
                    "retweet_count": 3013
                },
                "text": "Lock in! #DubNation"
            },
            "1": {
                "id": 1627135618030632960,
                "metrics": {
                    "bookmark_count": 187,
                    "impression_count": 5392221,
                    "like_count": 61914,
                    "quote_count": 290,
                    "reply_count": 421,
                    "retweet_count": 3858
                },
                "text": "\u231a\ufe0f yessir get you one @Dame_Lillard  congrats!!! Hahaha he said he retiring from it with the trophy in the hand \ud83d\ude02\ud83d\ude02 I feel you"
            },
            "2": {
                "id": 1627149382981406727,
                "metrics": {
                    "bookmark_count": 401,
                    "impression_count": 14600755,
                    "like_count": 102883,
                    "quote_count": 200,
                    "reply_count": 448,
                    "retweet_count": 6175
                },
                "text": "Man was a viral HOH high school dunk phenom, still working his way to the League, but lemme go get that dunk contest trophy right quick and bring it back to life!!! Unreal #macmclung"
            },
            "3": {
                "id": 1623185534301655040,
                "metrics": {
                    "bookmark_count": 785,
                    "impression_count": 14174566,
                    "like_count": 326030,
                    "quote_count": 1193,
                    "reply_count": 1187,
                    "retweet_count": 33328
                },
                "text": "Congrats @KingJames \u2026legendary stuff right there \ud83e\udee1 #38388"
            }
        },
        "stephenasmith": {
            "0": {
                "id": 1652797207270281216,
                "metrics": {
                    "bookmark_count": 141,
                    "impression_count": 1280353,
                    "like_count": 23778,
                    "quote_count": 135,
                    "reply_count": 369,
                    "retweet_count": 3191
                },
                "text": "This, ladies &amp; Gentlemen, is unreal. @StephenCurry30\u2026.the greatest Game 7 performance ever. At age 35. Walking into timeout chanting \u201cthey can\u2019t finish.\u201d This is just special. I called the outcome \u2014 but not like this. Lord Have Mercy\ud83d\ude00"
            },
            "1": {
                "id": 1683854222876368897,
                "metrics": {
                    "bookmark_count": 53,
                    "impression_count": 1785062,
                    "like_count": 38154,
                    "quote_count": 52,
                    "reply_count": 299,
                    "retweet_count": 2289
                },
                "text": "Good Lord. Just heard about Bronny. Hearing he\u2019s okay. Thank God! Prayers up to @KingJames and the entire family. #\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe"
            },
            "2": {
                "id": 1614480276381384706,
                "metrics": {
                    "bookmark_count": 126,
                    "impression_count": 3833824,
                    "like_count": 35592,
                    "quote_count": 668,
                    "reply_count": 1446,
                    "retweet_count": 4488
                },
                "text": "Congratulations @SeanPayton. Welcome to Los Angeles as the new coach is the @chargers. There is no way Brandon Staley can keep his job after blowing this lead. There\u2019s no coming back from this for him!"
            },
            "3": {
                "id": 1610117980913909762,
                "metrics": {
                    "bookmark_count": 44,
                    "impression_count": 2849377,
                    "like_count": 48486,
                    "quote_count": 54,
                    "reply_count": 590,
                    "retweet_count": 2352
                },
                "text": "Damn, this is scary. Prayers up for @BuffaloBills Safety Damar Hamlin \u2014 who\u2019s in critical condition. Just praying this brother survives and ends up okay.#\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe\ud83d\ude4f\ud83c\udffe"
            }
        }
    }

    const [currentIndex, setCurrentIndex] = useState(0);

    const users = Object.keys(tweetsByUser);

    const handlePrev = () => {
        setCurrentIndex((prevIndex) => (prevIndex === 0 ? users.length - 1 : prevIndex - 1));
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex === users.length - 1 ? 0 : prevIndex + 1));
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-4">
                <button onClick={handlePrev} className="text-gray-500 hover:bg-gray-100 rounded-full py-3 px-6">
                    Prev
                </button>
                <h2 className="text-2xl font-bold flex items-center">{users[currentIndex]} 
                    <Button className = "hover:bg-gray-800 border border-opacity-100 px-3 py-1 rounded-full border-black bg-black text-white text-sm ml-4"> 
                        Follow 
                    </Button></h2>
                <button onClick={handleNext} className="text-gray-500 hover:bg-gray-100 rounded-full py-3 px-5">
                    Next
                </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.values(tweetsByUser[users[currentIndex]]).map((tweet, idx) => (
                    <div key={idx} className="bg-blue-100 p-4 rounded-lg shadow">
                        <p className="font-semibold">{tweet.text}</p>

                        <div className="flex items-end justify-center gap-3">
                            <Button className="rounded-full p-1 hover:bg-green-100">
                                <FaRetweet />
                            </Button>
                            <p className="text-gray-500 text-sm mt-2 rounded-full p-1 hover:bg-transparent">@{users[currentIndex]}</p>
                            <Button className="rounded-full p-1 hover:bg-red-100">
                                <IoMdHeartEmpty />
                            </Button>
                        </div>

                    </div>
                ))}
            </div>
            <div className="mt-10">
                <div className="animate-pulse">
                    Game Over.
                </div>
            </div>
        </div>
    );

}

