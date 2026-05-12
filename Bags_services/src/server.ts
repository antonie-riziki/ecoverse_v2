import express from "express";
import dotenv from "dotenv";
import { launchEcoVerseToken } from "./launchToken";

dotenv.config({ path: "../.env" });

const app = express();
app.use(express.json());

app.post("/launch-token", async (req, res) => {
  try {
    const result = await launchEcoVerseToken(req.body);
    res.json({ success: true, result });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || "Token launch failed",
    });
  }
});

app.listen(8787, () => {
  console.log("Bags service running on http://localhost:8787");
});