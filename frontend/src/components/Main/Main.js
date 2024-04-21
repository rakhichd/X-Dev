import Button from "../Button/Button";
import DoneScreen from "../DoneScreen/DoneScreen";
import StartPage from "../StartPage/StartPage.js";
import React, { useState, useEffect } from "react";
import { FaUserFriends } from "react-icons/fa";
import { setGlobalState } from "../../state/state";
import getTweets from "../../api/getTweets";
import getHint from "../../api/getHint.js";

export default function Main() {
  const [mistakesRemaining, setMistakesRemaining] = useState(4);
  const [selectedTiles, setSelectedTiles] = useState([]);
  const [correctTiles, setCorrectTiles] = useState([]);
  const [incorrectTiles, setIncorrectTiles] = useState([]);
  const [done, setDone] = useState(false);
  const [oneAway, setOneAway] = useState(false);
  const [start, setStart] = useState(true);
  const [hint, setHint] = useState("");

  function shuffle(array) {
    const shuffledArray = [...array];
    for (let i = shuffledArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffledArray[i], shuffledArray[j]] = [
        shuffledArray[j],
        shuffledArray[i],
      ];
    }
    return shuffledArray;
  }

  const handleHint = async () => {
    const rand = Math.floor(Math.random() * incorrectTiles.length);
    const user = incorrectTiles[rand];
    const { resultJson } = await getHint(user);
    setHint(resultJson.hint);
  };

  const shuffleBoard = () => {
    setIncorrectTiles((prev) => shuffle(prev));
  };

  function deselectAll() {
    return setSelectedTiles([]);
  }

  const selectTweetTile = (id) => {
    setSelectedTiles((prev) => {
      if (prev.includes(id)) {
        return prev.filter((tileId) => tileId !== id);
      } else if (prev.length < 4) {
        return [...prev, id];
      }
      return prev;
    });
  };
  function MistakesRemaining() {
    return (
      <div className="flex gap-1 items-center">
        {Array.from({ length: mistakesRemaining }).map((_, index) => (
          <div key={index} className="rounded-full h-4 w-4 bg-gray-500"></div>
        ))}
      </div>
    );
  }

  function correctGuess() {
    const allGtiles = incorrectTiles.filter((tweet) =>
      selectedTiles.includes(tweet.id)
    );
    const corr = correctTiles.concat(allGtiles);
    setCorrectTiles(corr);
    const allStillWrong = incorrectTiles.filter(
      (tweet) => !corr.map((t) => t.id).includes(tweet.id)
    );
    console.log(allStillWrong)
    if (allStillWrong.length == 0) {
        console.log("hi")
        setDone(true)
    }
    setIncorrectTiles(allStillWrong);
    setSelectedTiles([]);
    if (allStillWrong.length < 4) {
        setDone(true);
    }
  }
  console.log(done);

  function submitGuesses() {
    const arrG = incorrectTiles.filter((tweet) =>
      selectedTiles.includes(tweet.id)
    );
    const users = arrG.map((tweet) => tweet.user);
    if (arrG.length === 4) {
      if (users.every((user) => user === users[0])) {
        correctGuess();
        if (incorrectTiles.length === 4) {
            setDone(true);
        }
        return true;
      } else {
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
        setMistakesRemaining(mistakesRemaining - 1);
        if (mistakesRemaining === 1) {
            setDone(true);
      }
    }
    return false;
  }
}

  const CustomizeButton = ({ width }) => {
    return (
      <button
        className={`mt-5 flex flex-row items-center bg-black bg-opacity-10 p-2 rounded-[4px] mb-[6px] border border-white border-opacity-10 hover:bg-opacity-[.15] `}
        onClick={() => {
          setGlobalState("showAddPeople", true);
          setGlobalState("showSideBar", false);
        }}
      >
        <FaUserFriends className="text-lg w-[24px] text-[#7289da] mr-2" />
        <span className="whitespace-nowrap overflow-hidden">
          <span className="text-black font-semibold">Customize</span>
        </span>
      </button>
    );
  };

  return (
    <div className="max-w-[100rem] ml-auto mr-auto flex flex-col items-center">
      {!done ? (
        <>
          {start ? (
            <>
              <StartPage
                setStart={setStart}
                setIncorrectTiles={setIncorrectTiles}
                shuffle={shuffle}
              ></StartPage>
            </>
          ) : (
            <>
              {oneAway && <div className="fade-out mt-6">One Away...</div>}
              {hint && (
                <div className="fixed right-10 bottom-10 z-[999] fadeIn bg-gray-200 px-5 py-3 text-black rounded-md">
                  {hint}
                </div>
              )}
              <div className="grid gap-3 grid-cols-4 px-3 py-4 mt-7">
                {correctTiles.slice(0, 4).map((tweet) => (
                  <Button
                    key={tweet.id}
                    className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-pink-100"
                    onClick={() => selectTweetTile(tweet.id)}
                  >
                    {tweet.text}
                  </Button>
                ))}
                {correctTiles.slice(4, 8).map((tweet) => (
                  <Button
                    key={tweet.id}
                    className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-green-100"
                    onClick={() => selectTweetTile(tweet.id)}
                  >
                    {tweet.text}
                  </Button>
                ))}
                {correctTiles.slice(8, 12).map((tweet) => (
                  <Button
                    key={tweet.id}
                    className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-yellow-100"
                    onClick={() => selectTweetTile(tweet.id)}
                  >
                    {tweet.text}
                  </Button>
                ))}
                {correctTiles.slice(12).map((tweet) => (
                  <Button
                    key={tweet.id}
                    className="py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md bg-purple-100"
                    onClick={() => selectTweetTile(tweet.id)}
                  >
                    {tweet.text}
                  </Button>
                ))}
                {incorrectTiles.map((tweet) => (
                  <Button
                    key={tweet.id}
                    className={`py-3 px-1 rounded-lg overflow-scroll h-20 w-13 max-w-md ${
                      selectedTiles.includes(tweet.id)
                        ? "bg-blue-100"
                        : "bg-gray-100"
                    }`}
                    onClick={() => selectTweetTile(tweet.id)}
                  >
                    {tweet.text}
                  </Button>
                ))}
              </div>

              <div className="inline-block">
                <div className="py-3 flex gap-2 ">
                  {" "}
                  <h1> Mistakes Remaining: </h1> <MistakesRemaining />{" "}
                </div>
              </div>

              <div className="flex gap-2 place-content-center">
                <Button
                  className={
                    "active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"
                  }
                  onClick={shuffleBoard}
                >
                  Shuffle
                </Button>
                <Button
                  className={
                    "active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"
                  }
                  onClick={deselectAll}
                >
                  Deselect All
                </Button>
                <Button
                  className={
                    "active:bg-blue-500 border border-opacity-100 px-6 py-2 rounded-full border-black"
                  }
                  onClick={submitGuesses}
                >
                  Submit
                </Button>
                <Button
                  className={
                    "active:bg-blue-500 border border-opacity-100 px-6 py-2 rounded-full border-black"
                  }
                  onClick={handleHint}
                >
                  ?
                </Button>
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
  );
}
