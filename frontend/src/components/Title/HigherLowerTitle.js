import { BsTwitterX } from "react-icons/bs";
import { RxDividerVertical } from "react-icons/rx";

export default function HigherLowerTitle() {
  return (
    // <>
      <div className="flex gap-1 ml-auto mr-auto items-center">
        <BsTwitterX className="text-[40px]"/>
        <RxDividerVertical className="text-[60px] ml-[-20px] mr-[-20px]"/>
        <span className="font-semibold text-5xl">Higher or Lower</span>
      </div>
    // </>
  );
}
