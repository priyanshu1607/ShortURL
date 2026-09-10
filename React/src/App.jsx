import { BrowserRouter, Routes, Route } from "react-router-dom"

import "./App.css"
import CreateURL from "./pages/URLRouter"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CreateURL />} />
        </Routes>
    </BrowserRouter>
  )
}

export default App