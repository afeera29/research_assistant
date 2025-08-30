import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchPapers = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const BACKEND_URL =process.env.NODE_ENV === "production"
      ? "https://research-assistant-0flj.onrender.com"
      : "http://127.0.0.1:8000";
  const res = await axios.get(`${BACKEND_URL}/search`, { params: { query } });


      setResults(Array.isArray(res.data.results) ? res.data.results : []);
    } catch (err) {
      console.error(err);
      setResults([]);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-4xl font-bold text-blue-600 mb-6">📚 Academic Research Assistant</h1>
      
      <div className="flex gap-2 mb-6 w-full max-w-xl">
        <input
          type="text"
          placeholder="Enter research topic..."
          className="flex-1 p-3 rounded-xl border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && searchPapers()}
        />
        <button 
          onClick={searchPapers}
          className="px-4 py-2 bg-blue-600 text-white rounded-xl shadow hover:bg-blue-700"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-gray-500 mb-4">Searching papers...</p>}

      <div className="w-full max-w-2xl space-y-4">
        {Array.isArray(results) && results.map((paper, idx) => (
          <div key={idx} className="p-4 bg-white rounded-xl shadow hover:shadow-lg transition">
            <h2 className="text-lg font-semibold text-gray-800">{paper.title}</h2>
            <p className="text-sm text-gray-500"> Author: {paper.author}</p>
            <p className="text-sm text-gray-500"> Date: {paper.date}</p>
            <a 
              href={paper.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline mt-2 inline-block"
            >
              🔗 Read Paper
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
