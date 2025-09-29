import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Train from "./pages/Train";
import Detect from "./pages/Detect";

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: "flex", gap: 15, padding: 10 }}>
        <Link to="/">Train</Link>
        <Link to="/detect">Detect</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Train />} />
        <Route path="/detect" element={<Detect />} />
      </Routes>
    </BrowserRouter>
  );
}
