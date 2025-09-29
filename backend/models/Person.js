const mongoose = require("mongoose");

const PersonSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, unique: true },
    label: { type: Number, required: true },
    samples: { type: Number, default: 0 },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Person", PersonSchema);
