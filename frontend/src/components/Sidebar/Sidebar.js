import useDimensions from "../../hooks/useDimensions";
import useSideBarListener from "../../hooks/useSideBarListener";
import { setGlobalState, useGlobalState } from "../../state/state";
import React from "react";
import CloseButton from "./CloseButton"
import MenuButton from "./MenuButton";
import { FaUserFriends } from "react-icons/fa";

const CustomizeButton = ({ width }) => {
  return (
    <button
      className={`flex flex-row w-full items-center bg-white bg-opacity-10 p-2 rounded-[4px] mb-[6px] border border-white border-opacity-10 hover:bg-opacity-[.15] `}
      onClick={() => {
        setGlobalState("showAddPeople", true)
        setGlobalState("showSideBar", false);
      }}
    >
      <FaUserFriends className="text-lg w-[24px] text-[#7289da] mr-2" />
      <span className="whitespace-nowrap overflow-hidden">
        <span className="text-white font-semibold">Customize</span>
        <span> - Play With Friends</span>
      </span>
    </button>
  )
}

const SideBar = () => {

  const { showSideBar, setShowSideBar } = useSideBarListener();
  const { width } = useDimensions()

  return <>
    <div
      className={`
        items-start fixed
        lg:items-end 
        duration-200
        ${showSideBar ? 'bg-black' : 'bg-white'}
        flex-col
        ${showSideBar && 'z-[102]'}
        ${showSideBar ? 'h-screen' : 'h-screen'}
        `}
      style={{
        width: showSideBar ? "290px" : "50px",
      }}
    >
      {!showSideBar && <MenuButton setShowSideBar={setShowSideBar} />}
      {showSideBar &&
        <>
          <div className="px-3 w-full h-full">
            <div className="text-gray-400 text-[16px] w-full">
              <CloseButton setShowSideBar={setShowSideBar}/>
            </div>
            <div
              className="text-gray-400 text-[15px] w-full"
              style={{
                bottom: 20,
                left: 12
              }}
            >
              <CustomizeButton width={width - 24} />
            </div>
          </div>
        </>
      }
    </div>
  </>
}

export default React.memo(SideBar);