import "./App.css";
import { Sidebar, Main, Title } from "./components";

function App() {
  return (
    <div className="App">
      <div>
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
