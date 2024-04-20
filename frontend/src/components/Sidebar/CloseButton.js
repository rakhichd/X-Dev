import { HiOutlineChevronDoubleLeft } from "react-icons/hi";
import { setGlobalState } from "../../state/state";

export default function CloseButton() {
  return (
      <div
        ID="sidebar-btn-close"
        onClick={() => {
          setGlobalState("showSideBar", false);
        }}
        style={{ height: 30.5 }}
        className={`hover:bg-white hover:bg-opacity-20 rounded-[4px] p-1 px-[6px] text-gray-800 grid place-content-center cursor-pointer`}
      >
        <HiOutlineChevronDoubleLeft className="text-gray-300 text-xl" />
      </div>
  );
}
