const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: "uploads/" });

/* ---------- UPLOAD EVIDENCE ---------- */
app.post("/upload", upload.single("video"), (req, res) => {
  const { caseId, evidenceId } = req.body;
  const videoPath = req.file.path;

  const cmd = `python ../insert.py ${caseId} ${evidenceId} ${videoPath}`;

  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.error(stderr);
      return res.status(500).json({ error: stderr });
    }
    res.json({ success: true, output: stdout });
  });
});

/* ---------- VERIFY EVIDENCE ---------- */
app.post("/verify", upload.single("video"), (req, res) => {
  const videoPath = req.file.path;
  const cmd = `python ../verifyBlock.py ${videoPath}`;

  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      return res.status(400).json({ tampered: true, output: stderr });
    }
    res.json({ tampered: false, output: stdout });
  });
});

app.listen(5000, () => {
  console.log("✅ Backend running on http://localhost:5000");
});
