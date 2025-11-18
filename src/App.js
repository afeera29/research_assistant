import React, { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      // OLD: fetch(`http://127.0.0.1:8000/search?query=...`)
      
      // NEW: Use the relative path defined in index.py
      const response = await fetch(
        `/api/search?query=${encodeURIComponent(query)}`
      );
      
      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error("Error fetching:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-6 bg-gradient-to-b from-white to-gray-100">
      <h1 className="text-4xl font-bold mb-8 text-gray-900 mt-10">
        🔍 Research Assistant
      </h1>

      <div className="w-full max-w-xl flex gap-2">
        <input
          className="flex-1 px-4 py-3 rounded-xl border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Search academic papers (e.g. AI, sustainability)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-5 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      <div className="mt-10 w-full max-w-3xl grid grid-cols-1 md:grid-cols-2 gap-6">
        {results.map((paper, idx) => (
          <div
            key={idx}
            className="bg-white p-5 rounded-2xl shadow hover:shadow-lg transition"
          >
            <h3 className="font-semibold text-lg text-gray-900 mb-2">
              {paper.title}
            </h3>
            <p className="text-sm text-gray-600 mb-2">
              {paper.author || "Unknown Author"}
            </p>
            <p className="text-xs text-gray-400 mb-3">
              {paper.date ? new Date(paper.date).toLocaleDateString() : ""}
            </p>
            <a
              href={paper.url}
              target="_blank"
              rel="noreferrer"
              className="text-blue-600 hover:underline font-medium"
            >
              Read Paper →
            </a>
          </div>
        ))}
      </div>

      {results.length === 0 && !loading && (
        <p className="mt-20 text-gray-400 italic">
          Start by searching for a topic above.
        </p>
      )}
    </div>
  );
}
