const express = require("express");
const path = require("path");
const { spawn } = require("child_process");
const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const pyCommand = process.env.PYTHON || "python";
    const scriptPath = path.resolve(__dirname, "../../python/train_model.py");

    const child = spawn(pyCommand, [scriptPath], {
      cwd: path.resolve(__dirname, "../../python"),
    });

    let output = "";
    let errorOutput = "";

    child.stdout.on("data", (data) => {
      output += data.toString();
    });

    child.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    child.on("close", (code) => {
      if (code === 0 && output.includes("TRAIN_OK")) {
        return res.json({ ok: true });
      }
      console.error("Train script failed", code, errorOutput, output);
      res.status(500).json({ ok: false, code, errorOutput, output });
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "train_failed" });
  }
});

module.exports = router;
