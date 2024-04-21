import "./App.css";
import Connections from "./pages/Connections";
import HigherLower from "./pages/HigherLower";
import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";

function App() {
  return (
    <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/whosaidthat" element={<Connections />} />
        <Route path="/higherlower" element={<HigherLower />} />
      </Routes>
  );
}

export default App;
