import "./App.css";
import Connections from "./pages/Connections";
import HigherLower from "./pages/HigherLower";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
      <Routes>
        <Route path="/whosaidthat" element={<Connections />} />
        <Route path="/higherlower" element={<HigherLower />} />
      </Routes>
  );
}

export default App;
