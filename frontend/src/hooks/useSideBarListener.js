import { setGlobalState, useGlobalState } from "../state/state";

const useSideBarListener = () => {

    const [showSideBar, setShowSideBar] = useGlobalState("showSideBar");

    return {
        showSideBar,
        setShowSideBar,
    }
}

export default useSideBarListener;