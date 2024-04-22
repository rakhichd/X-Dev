import { createGlobalState } from "react-hooks-global-state";

const { setGlobalState, useGlobalState, getGlobalState } = createGlobalState({
  showSideBar: false,
  showAddPeople: false,
  people: [],
  startDate: "2023",
  tweets: {}
});

export { getGlobalState, setGlobalState, useGlobalState };
