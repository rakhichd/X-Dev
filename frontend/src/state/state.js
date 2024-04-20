import { createGlobalState } from "react-hooks-global-state";

const { setGlobalState, useGlobalState, getGlobalState } = createGlobalState({
  showSideBar: true,
});

export { getGlobalState, setGlobalState, useGlobalState };
