import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from exa_py import Exa

# Load .env
load_dotenv()

# Read API key from environment
exa_api_key = os.getenv("EXA_API_KEY")
exa = Exa(exa_api_key)

app = FastAPI()

# Serve React build
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")

@app.get("/")
def serve_react():
    return FileResponse("../frontend/build/index.html")

# Your /search endpoint
@app.get("/search")
def search_papers(query: str = Query(...)):
    try:
        response = exa.search(
            query,
            num_results=10,
            category="papers",
            start_published_date="2020-01-01",
            include_domains=[
                "arxiv.org",
                "researchgate.net",
                "springer.com",
                "ieee.org",
                "acm.org"
            ]
        )

        results = []
        for r in response.results:
            results.append({
                "title": r.title or "N/A",
                "author": r.author or "N/A",
                "date": getattr(r, "published_date", "N/A"),
                "url": r.url or "N/A"
            })
        return {"results": results}

    except Exception as e:
        print("Exa API error:", e)
        return {"results": [], "error": str(e)}
