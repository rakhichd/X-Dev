import { Sidebar } from "../components";
import { HigherLowerTitle, HigherLowerContent } from "../components";
import { BsTwitterX } from "react-icons/bs";

export default function HigherLower() {
  return (
    <div className="flex relative h-screen">
      <Sidebar />
      <div className="flex-grow relative ml-[80px] flex flex-col items-center ">
        <HigherLowerTitle />
        <HigherLowerContent />
        <div className="left-[80px] fixed inset-0 flex justify-center items-center mt-[100px]">
          <div className="w-[2px] bg-gray-500 h-full absolute"></div>
          <div className="bg-white z-[10]">
            <BsTwitterX size={40} />
          </div>
        </div>
      </div>
    </div>
  );
}
