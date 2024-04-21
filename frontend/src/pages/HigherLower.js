import { Sidebar } from "../components";
import { HigherLowerTitle, HigherLowerContent } from "../components";
import { BsTwitterX } from "react-icons/bs";
import { useState } from "react";
import StartHighLow from "../components/HigherLowerContent/StartHighLow";

export default function HigherLower() {
  const [start, setStart] = useState(false);
  const [posts, setPosts] = useState([])

  return (
    <div className="flex relative h-screen">
      <Sidebar />
      <div className="flex-grow relative ml-[80px] flex flex-col items-center ">
        <HigherLowerTitle />
        {start && (
          <>
            <HigherLowerContent posts={posts}/>
            <div className="left-[80px] fixed inset-0 flex justify-center items-center mt-[100px]">
              <div className="w-[2px] bg-gray-500 h-full absolute"></div>
              <div className="bg-white z-[10]">
                <BsTwitterX size={40} />
              </div>
            </div>
          </>
        )}
        {!start && <div><StartHighLow setStart={setStart} setPosts={setPosts}/></div>}
      </div>
    </div>
  );
}
