import Button from "../Button/Button"
import React, {useState, useEffect} from "react"

export default function Main() {
    
    const tweetsByUser = {
        "User1": [
            "Just finished a great workout 💪 #fitness #motivation",
            "Excited to announce our new product launch next week! Stay tuned for updates. #newproduct #launch",
            "Had an amazing time hiking with friends this weekend 🏞️ #nature #adventure",
            "Feeling grateful for all the wonderful people in my life. #gratitude #blessed"
        ],
        "User2": [
            "The quick brown fox jumps over the lazy dog.",
            "Life is like a box of chocolates.",
            "Keep calm and carry on.",
            "Where there is love, there is life."
        ],
        "User3": [
            "Another day, another adventure! #wanderlust #explore",
            "Just finished a book that left me speechless. Highly recommend! #booklover",
            "Feeling inspired after attending a coding workshop. #coding #inspiration",
            "Grateful for the little things that make life beautiful. #gratitude"
        ],
        "User4": [
            "Enjoying the simple moments in life. #simplepleasures",
            "Excited to start a new project this week! #newbeginnings",
            "Reflecting on past experiences and looking forward to new adventures. #reflection",
            "Appreciating the beauty of nature all around us. #naturelover"
        ]
    };

    const allTweets = [] // tweets put into an arr to make it easier to randomize 

    for (const user in tweetsByUser) {
        const tweets = tweetsByUser[user];
        for (const tweet of tweets) {
            allTweets.push(tweet);
        }
    }

    const [mistakesRemaining, setMistakesRemaining] = useState(4);
    const [selectedTiles, setSelectedTiles] = useState([]);
    const [categoriesRemaining, setCategoriesRemaining] = useState(4);
    const [shuffledTweets, setShuffledTweets] = useState(allTweets);

    const shuffle = (array) => { 
        return array.map((a) => ({ sort: Math.random(), value: a }))
            .sort((a, b) => a.sort - b.sort)
            .map((a) => a.value); 
    }; 

    const shuffleBoard = () => {
        console.log('hi')
        setShuffledTweets(shuffle(allTweets));
    };

    console.log(shuffledTweets)

    function deselectAll() {
        return "deselecting all"
        // all the selected tiles should reset to og color
        // reset the selectedTiles to empty array 
    }

    function submitGuesses() {
        return "submit Guesses"
        // if correct --> makes all the tiles the same color and send it to the top row, categoriesReamining +=1 
        // if wrong, decreases mistakes remaining, call deselectAll, 
        // if game over call game over function --> happens when categories reminaing = 0 or mistakesremindig = 0
    }

    function selectTweetTile() {
        return "select Tweet Tile"
        // change color of tweet to darker blue 
        // add to arr of selectedTiles 
    }

    function MistakesRemaining() { // num of dots to show up based on how many mistakes are remaining 
        return (
            <div className="flex gap-1 items-center">
                {Array.from({ length: mistakesRemaining }).map((_, index) => (
                    <div key={index} className="rounded-full h-4 w-4 bg-gray-500"></div>
                ))}
            </div>
            );
    }

    return (
        <div className="max-w-[100rem] ml-auto mr-auto">
            <div className = "grid gap-3 grid-cols-4 grid-cols-4 px-3 py-4"> 
                {shuffledTweets.map(tweet => <Button className={"py-3 px-1 rounded-lg bg-blue-100 overflow-scroll h-20 w-13 max-w-md"} onClick = {selectTweetTile}>{tweet}</Button>)}
            </div>

            <div className="inline-block">
                <div className="py-3 flex gap-2 "> <h1> Mistakes Remaining: </h1> <MistakesRemaining/> </div>
            </div>

            <div className = "flex gap-2 place-content-center">
                <Button className={"active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick ={shuffleBoard}>Shuffle</Button>
                <Button className={"active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick ={deselectAll}>Deselect All</Button>
                <Button className={"active:bg-blue-500 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick ={submitGuesses}>Submit</Button>
            </div>
        </div>
    )
}