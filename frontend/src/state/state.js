import { createGlobalState } from "react-hooks-global-state";

const { setGlobalState, useGlobalState, getGlobalState } = createGlobalState({
  showSideBar: false,
  showAddPeople: false,
  people: []
});

export { getGlobalState, setGlobalState, useGlobalState };
