import { Sidebar } from "../components";
import { HigherLowerTitle, HigherLowerContent } from "../components";
import { BsTwitterX } from "react-icons/bs";
import { useState } from "react";
import StartHighLow from "../components/HigherLowerContent/StartHighLow";
import HigherLowerDone from "../components/DoneScreen/HigherLowerDone";

export default function HigherLower() {
  const [start, setStart] = useState(false);
  const [posts, setPosts] = useState([]);
  const [done, setDone] = useState(false);
  const [score, setScore] = useState(0);

  return (
    <div className="flex relative h-screen">
      <Sidebar />
      <div className="flex-grow relative ml-[80px] flex flex-col items-center ">
        <HigherLowerTitle />
        {start && !done && (
          <>
            <h1 className="text-xl">Score: {score}</h1>
            <HigherLowerContent
              posts={posts}
              setDone={setDone}
              setScore={setScore}
              score={score}
            />
            <div className="left-[80px] fixed inset-0 flex justify-center items-center mt-[100px] z-[-1]">
              <div className="w-[2px] bg-gray-500 h-full absolute"></div>
              <div className="bg-white z-[10]">
                <BsTwitterX size={40} />
              </div>
            </div>
          </>
        )}
        {!start && !done && (
          <div>
            <StartHighLow setStart={setStart} setPosts={setPosts} />
          </div>
        )}
        {done && (
          <HigherLowerDone
            won={score == posts.length - 1}
            posts={posts.slice(0, score + 1)}
            score={score}
          />
        )}
      </div>
    </div>
  );
}
