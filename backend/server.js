const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: "uploads/" });

/* ---------- UPLOAD EVIDENCE ---------- */
app.post("/upload", upload.single("video"), (req, res) => {
  const { caseId, evidenceId } = req.body;
  const videoPath = req.file.path;

  const pythonExe = path.join(__dirname, "..", "venv", "Scripts", "python.exe");
  const scriptPath = path.join(__dirname, "..", "insert.py");
  const quoted = (s) => `"${s.replace(/"/g, '\\"')}"`;
  const cmd = `${quoted(pythonExe)} ${quoted(scriptPath)} ${quoted(caseId)} ${quoted(evidenceId)} ${quoted(videoPath)}`;

  exec(cmd, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
    if (error) {
      console.error(stderr || error.message);
      return res.status(500).json({ error: stderr || error.message });
    }
    res.json({ success: true, output: stdout });
  });
});

/* ---------- VERIFY EVIDENCE ---------- */
app.post("/verify", upload.single("video"), (req, res) => {
  const videoPath = req.file.path;
  const pythonExe = path.join(__dirname, "..", "venv", "Scripts", "python.exe");
  const scriptPath = path.join(__dirname, "..", "verifyBlock.py");
  const quoted = (s) => `"${s.replace(/"/g, '\\"')}"`;
  const cmd = `${quoted(pythonExe)} ${quoted(scriptPath)} ${quoted(videoPath)}`;

  exec(cmd, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
    if (error) {
      return res.status(400).json({ tampered: true, output: stderr });
    }
    res.json({ tampered: false, output: stdout });
  });
});

app.listen(5000, () => {
  console.log("✅ Backend running on http://localhost:5000");
});
