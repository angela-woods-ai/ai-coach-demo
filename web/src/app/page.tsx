"use client";

import { useState } from "react";

type CoachingResponse = {
  message: string;
  follow_up_questions: string[];
};

type RelevantReflection = {
  text: string;
  timestamp: string;
};

export default function Home() {
  const [text, setText] = useState(""); // Reflection text the user enters
  const [coaching, setCoaching] = useState<CoachingResponse | null>(null);
  const [count, setCount] = useState(0); // Reflection count - init to 0
  const [current_reflection, setCurrent] = useState<any>(null) // Most recent reflection
  const [relevant, setRelevant] = useState<RelevantReflection[]>([]) //  most relevant reflections
  const [memory_updated, setMemoryUpdated] = useState(false); // Was memory updated this turn? Set to false
  const [memory_summary, setMemorySummary] = useState<any>(null); // Most recent memory summary
  const [response, setResponse] = useState<any>(null); // Full response for debug printing
  const [loading, setLoading] = useState(false);
  
  async function submitReflection() {
    setLoading(true);
    setResponse(null);

    const res = await fetch("http://localhost:3001/api/process_reflection", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        idx: count + 1,
        text,
      }),
    });

    const data = await res.json();

    
    // Parts of the response for user display
    setCoaching(data.coaching);

    // Parts of the response for debug/behind the scenes view
    setResponse(data); // Full object for debug prints
    setCurrent(data.context.current_reflection.text)
    setRelevant(data.context.relevant_reflections)
    setCount(data.reflection_count);  
    setMemorySummary(data.context.memory_summary) 
    setMemoryUpdated(data.memory_updated) 

    // Reset to be ready to enter the next reflection
    setText("");
    setLoading(false);
  }

  async function handleClear() {
    try {
      const res = await fetch("http://localhost:3001/api/clear_memory", {
        method: "POST",
      });

      if (!res.ok) {
        throw new Error("Failed to clear");
      }

      // Clear UI state
      setText("");
      setCount(0);
      setResponse(null);
      setCurrent(null);
      setRelevant([]);
      setCoaching(null);
      setMemorySummary(null);
      setMemoryUpdated(false);

      alert("Memory cleared");
    } catch (err) {
      console.error(err);
      alert("Error clearing memory");
    }
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>AI Coach Demo</h1>
      
      {/* Enter reflections with text area + button to submit */}
      <textarea
        rows={4}
        style={{ width: "100%" }}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Write a reflection..."
      />

      <button onClick={submitReflection} disabled={loading}>
        {loading ? "Thinking..." : "Submit"}
      </button>

       {coaching && (
         <>
           <h3>Coaching Response</h3>
           <p>{coaching.message}</p>
           <ul style={{ marginLeft: "1.5rem", marginTop: "0.5rem "}}>
             {coaching.follow_up_questions.map((q, i) => (
               <li key={i}>{q}</li>
             ))}
           </ul>
         </>
       )}

      {/* Separator */}
      <hr style={{ margin: "2rem 0" }} />

      {/* Put the debug stuff in a little container */}
      <div
        style={{
          marginTop: "2rem",
          padding: "1rem",
          background: "#f5f5f5",
          borderRadius: "6px",
          fontSize: "0.9rem"
        }}
      >
      <h2> Behind the scenes (peek into how the AI works) </h2>

      {/* Clear button */}
      <button
        onClick={handleClear}
        style={{ marginBottom: 16 }}
      >
        Clear User Memory
      </button>

      <p>
        <strong>Reflection count:</strong> {count}
      </p>

      <div>
        <strong>Current reflection:</strong>
        <p style={{ marginLeft: 8, fontStyle: "italic" }}>
          {current_reflection ?? "—"}
        </p>
      </div>


      <p>
        <strong>Most relevant reflections:</strong>
      </p>
      <ul style={{ marginLeft: "1.5rem" }}>
        {relevant.map((r, i) => (
          <li key={i}>{r.text}</li>
        ))}
      </ul>

    <p>
        <strong>Memory summary updated this reflection:</strong>{" "}
        <span style={{ color: memory_updated ? "green" : "gray" }}>
          {memory_updated ? "Yes" : "No"}
        </span>
    </p>

     {/* Render memory summary as a block so it wraps nicely if it grows  */}
      <div>
        <strong>Most recent memory summary:</strong>
        <p style={{ marginLeft: 8, fontStyle: "italic" }}>
          {memory_summary ?? "—"}
        </p>
      </div>

      {/* Simple text dump of the AI response to the reflection submit - uncomment if I need to debug*/}
      {/* {response && (
        <pre style={{ marginTop: 16 }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )} */}

      </div>
    </main>
  );
}
