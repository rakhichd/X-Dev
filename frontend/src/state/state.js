import { createGlobalState } from "react-hooks-global-state";

const { setGlobalState, useGlobalState, getGlobalState } = createGlobalState({
  showSideBar: false,
});

export { getGlobalState, setGlobalState, useGlobalState };
