const express = require("express");
const fs = require("fs");
const path = require("path");
const router = express.Router();
const Person = require("../models/Person");

const DATASET_DIR = process.env.DATASET_DIR || "./storage/dataset";

// Ensure folder exists
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// POST /api/samples/capture
// body: { name: 'John', imageBase64: 'data:image/jpeg;base64,...' }
router.post("/capture", async (req, res) => {
  try {
    const { name, imageBase64 } = req.body;
    if (!name || !imageBase64) {
      return res.status(400).json({ error: "name and imageBase64 required" });
    }

    // Create or find person with label
    let person = await Person.findOne({ name });
    if (!person) {
      const count = await Person.countDocuments();
      person = await Person.create({
        name,
        label: count,
        samples: 0,
      });
    }

    const personDir = path.join(DATASET_DIR, person.name);
    ensureDir(personDir);

    const nextIndex = person.samples + 1;
    const filename = path.join(
      personDir,
      String(nextIndex).padStart(4, "0") + ".jpg"
    );

    // Remove base64 header
    const base64Data = imageBase64.replace(
      /^data:image\/(png|jpeg);base64,/,
      ""
    );
    fs.writeFileSync(filename, Buffer.from(base64Data, "base64"));

    person.samples = nextIndex;
    await person.save();

    res.json({ ok: true, samples: person.samples });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "capture_failed" });
  }
});

module.exports = router;
