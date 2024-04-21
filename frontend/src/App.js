import "./App.css";
import { Sidebar, Main, Title } from "./components";
import { useGlobalState } from "./state/state";
import { AddPeople } from "./components";

function App() {
  const [showAddPeople] = useGlobalState("showAddPeople");

  console.log(showAddPeople)

  return (
    <div className="App">
      <div>
        {showAddPeople && <AddPeople />}
        <Sidebar />
        <div className="ml-[80px] flex flex-col">
          <Title />
          <Main />
        </div>
      </div>
    </div>
  );
}

export default App;
