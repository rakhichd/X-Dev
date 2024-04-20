import Button from "../Button/Button"
import React, {useState, useEffect} from "react"

export default function Main() {


    const tweetsByUser = {
        "elden" : [{id : "1", text: "one edlen"},
                    {id : "2", text: "two elden"},
                    {id : "3", text: "three elden"},
                    {id : "4", text: "four elden"}],
        "rakhi" : [{id : "5", text: "one rakhi"},
                    {id : "6", text: "two rakhi"},
                    {id : "7", text: "three rakhi"},
                    {id : "8", text: "four rakhi"}],
        "matthew" : [{id : "9", text: "one matthew"},
                    {id : "10", text: "two matthew"},
                    {id : "11", text: "three matthew"},
                    {id : "12", text: "four matthew"}],
        "lucas" : [{id : "13", text: "one lucas"},
                    {id : "14", text: "two lucas"},
                    {id : "15", text: "three lucas"},
                    {id : "16", text: "four lucas"}],
    }

    // elonmusk[0].tweet.text 
    const allTweets = {} // tweets put into an arr to make it easier to randomize 

    for (const user in tweetsByUser) {
        const tweetObjects = tweetsByUser[user];
        for (const tweetObj of tweetObjects) {
            allTweets[tweetObj.id] = tweetObj.text;
        }
    }

    const shuffleObject = (obj) => {
        const keys = Object.keys(obj);
        const shuffledKeys = shuffle(keys);
        const shuffledObject = {};
        shuffledKeys.forEach(key => {
            shuffledObject[key] = obj[key];
        });
        return shuffledObject;
    };

    const shuffle = (array) => { 
        return array.map((a) => ({ sort: Math.random(), value: a }))
            .sort((a, b) => a.sort - b.sort)
            .map((a) => a.value); 
    }; 

    const shuffleBoard = () => {
        setShuffledTweets(shuffleObject(allTweets));
    };

    const [mistakesRemaining, setMistakesRemaining] = useState(4);
    const [selectedTiles, setSelectedTiles] = useState(new Set());
    const [categoriesRemaining, setCategoriesRemaining] = useState(4);
    const [shuffledTweets, setShuffledTweets] = useState(allTweets);

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

    const selectTweetTile = (index) => {
        setSelectedTiles(prev => {
            const updatedSet = new Set(prev); // Create a new set based on the previous set
            if (!updatedSet.has(index)) {
                updatedSet.add(index); // Add the index if it's not already in the set
            } else {
                updatedSet.delete(index); // Remove the index if it's already in the set
            }
            return updatedSet; // Return the updated set
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

    return (
        <div className="max-w-[100rem] ml-auto mr-auto">

            <div className="grid gap-3 grid-cols-4 grid-cols-4 px-3 py-4">
                {Object.keys(shuffledTweets).map(tweetID => (
                    <Button
                        key={tweetID}
                        className={`py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md ${selectedTiles.has(tweetID) ? "bg-blue-100" : "bg-gray-100"}`}
                        onClick={() => selectTweetTile(tweetID)}
                    >
                        {shuffledTweets[tweetID]}
                    </Button>
                ))}
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