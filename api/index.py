from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from exa_py import Exa
import os

app = FastAPI()

# CORS: Allow your React app to talk to this function
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EXA
# Ensure you add EXA_API_KEY in Vercel Settings -> Environment Variables
EXA_API_KEY = os.getenv("EXA_API_KEY")
exa = Exa(EXA_API_KEY)

@app.get("/api/search") 
def search_papers(query: str = Query(...)):
    try:
        response = exa.search(
            query=query,
            num_results=10,
            category="papers",
            start_published_date="2020-01-01",
            include_domains=["arxiv.org", "researchgate.net", "springer.com", "ieee.org", "acm.org"],
        )
        
        # Parse results safely
        results = []
        if hasattr(response, "results"):
            for r in response.results:
                results.append({
                    "title": getattr(r, "title", "N/A"),
                    "author": getattr(r, "author", "N/A"),
                    "date": getattr(r, "published_date", "N/A"),
                    "url": getattr(r, "url", "N/A"),
                })
        return {"results": results}
    except Exception as e:
        return {"results": [], "error": str(e)}