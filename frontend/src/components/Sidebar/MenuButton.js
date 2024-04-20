import { IoMdMenu } from "react-icons/io";

const MenuButton = ({ setShowSideBar, className }) => {


    return (
        <div style={{ height: 50 }} className="pt-[9px]">
            <div
                ID={"sidebar-open-btn"}
                onClick={() => {
                    setShowSideBar(true)
                }}
                style={{
                    height: 30.5
                }}
                className={`${'ml-3 hover:scale-x-125'} duration-200 rounded-[4px] p-1 px-[6px] text-gray-800 grid place-content-center ${className} cursor-pointer`}
            >
                <IoMdMenu className={`text-gray-500 text-[23px] ${className}`} />
            </div>
        </div>
    )
}

export default MenuButton;