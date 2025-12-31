import { useState } from "react";

const AddEvidence = () => {
  const [caseId, setCaseId] = useState("");
  const [evidenceId, setEvidenceId] = useState("");
  const [video, setVideo] = useState(null);
  const [msg, setMsg] = useState("");

  const uploadEvidence = async () => {
    const formData = new FormData();
    formData.append("caseId", caseId);
    formData.append("evidenceId", evidenceId);
    formData.append("video", video);

    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setMsg(JSON.stringify(data, null, 2));
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Add Evidence</h2>
      <input placeholder="Case ID" onChange={e => setCaseId(e.target.value)} />
      <br />
      <input placeholder="Evidence ID" onChange={e => setEvidenceId(e.target.value)} />
      <br />
      <input type="file" onChange={e => setVideo(e.target.files[0])} />
      <br />
      <button onClick={uploadEvidence}>Upload</button>
      <pre>{msg}</pre>
    </div>
  );
};

export default AddEvidence;
