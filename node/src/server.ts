// NodeJS Server that is the backend for frontend orchestrator that connects FastAPI (AI logic layer) and NextJS (UI layer)
// Currently NodeJS runs on localhost:3001 
// Curl can be used to make debug calls
import express from "express";
import axios from "axios";
import cors from "cors";

const app = express();
app.use(express.json());

// Keep cors from blocking UI calls to NodeJS
app.use(cors({
  origin: "http://localhost:3000",
}));

const FASTAPI_URL = "http://127.0.0.1:8000";

// ---- support testing server health with curl from terminal: curl http://localhost:3001/api/health 

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});


// ---- Calls that connect NextJS (UI) to NodeJS (Orchestrator) to FastAPI (AI logic layer)

app.post("/api/process_reflection", async (req, res) => {
  console.log("Incoming UI request", req.body);
  try {
    const { idx, text } = req.body;

    // Important to use the address rather than localhost to avoid the IPv6 issues
    const aiResponse = await fetch("http://127.0.0.1:8000/process_reflection", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        idx,
        text
      }),
    });

    if (!aiResponse.ok) {
      throw new Error("FastAPI error");
    }

    const data = await aiResponse.json();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Upstream AI service failed" });
  }
});

app.post("/api/clear_memory", async (req, res) => {
  try {
    const aiRes = await fetch("http://127.0.0.1:8000/clear_memory", {
      method: "POST",
    });

    if (!aiRes.ok) {
      throw new Error("AI service error");
    }

    const data = await aiRes.json();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to clear memory" });
  }
});

// ------ Debug calls that connect NodeJS (Orchestrator) to FAST API (AI logic layer), use for testing without the UI involved
// ------ Can call from curl direclty like this
// curl -X POST http://localhost:3001/internal/debug/process_reflection \
//               -H "Content-Type: application/json" \
//               -d '{
//                 "idx": 1,
//                 "text": "My test prhase"
//           }'

app.post("/internal/debug/process_reflection", async (req, res) => {
  try {
    const response = await axios.post(
      `${FASTAPI_URL}/process_reflection`,
      req.body
    );

    // For now: pass through unchanged
    res.json(response.data);
  } catch (err: any) {
    console.error(err?.response?.data || err.message);
    res.status(500).json({ error: "Upstream AI service failed" });
  }
});

app.post("/internal/debug/clear_memory", async (req, res) => {
  try {
    const response = await axios.post(
      `${FASTAPI_URL}/clear_memory`,
      req.body
    );

    // For now: pass through unchanged
    res.json(response.data);
  } catch (err: any) {
    console.error(err?.response?.data || err.message);
    res.status(500).json({ error: "Upstream AI service failed" });
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Node API running on http://localhost:${PORT}`);
});

