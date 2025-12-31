import { Route, Routes } from "react-router-dom";
import Login from "./Login";

import AddEvidence from "./AddEvidence";
import VerifyEvidence from "./VerifyEvidence";
import ViewEvidence from "./ViewEvidence";

const App = () => {
  return (
    <>
      <Routes>
        {/* Login */}
        <Route path="/" element={<Login />} />

        {/* Evidence Chain of Custody */}
        <Route path="/add-evidence" element={<AddEvidence />} />
        <Route path="/verify-evidence" element={<VerifyEvidence />} />
        <Route path="/view-evidence" element={<ViewEvidence />} />
      </Routes>
    </>
  );
};

export default App;
