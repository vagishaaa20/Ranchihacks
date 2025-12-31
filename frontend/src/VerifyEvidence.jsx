const VerifyEvidence = () => {
  const verify = async () => {
    const res = await fetch("http://localhost:5000/verify-evidence", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filePath: "evidence.bin" })
    });
    const data = await res.json();
    alert(data.result);
  };

  return <button onClick={verify}>Verify Evidence</button>;
};

export default VerifyEvidence;
