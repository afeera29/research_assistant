from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
from exa_py import Exa

# Load environment variables
load_dotenv()
EXA_API_KEY = os.getenv("EXA_API_KEY")
exa = Exa(EXA_API_KEY) 

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# React frontend build path
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/build")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Serve main React page
@app.get("/")
def serve_react():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Serve favicon and manifest
@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join(frontend_path, "favicon.ico"))

@app.get("/manifest.json")
def manifest():
    return FileResponse(os.path.join(frontend_path, "manifest.json"))

# Catch-all route for React Router
@app.get("/{full_path:path}")
def serve_react_catchall(full_path: str):
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Search API
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
        for r in getattr(response, "results", []):
            results.append({
                "title": getattr(r, "title", "N/A"),
                "author": getattr(r, "author", "N/A"),
                "date": getattr(r, "published_date", "N/A"),
                "url": getattr(r, "url", "N/A")
            })
        return {"results": results}

    except Exception as e:
        print("Exa API error:", e)
        return {"results": [], "error": str(e)}
@app.get("/debug")
def debug():
    return {"EXA_API_KEY": EXA_API_KEY, "frontend_exists": os.path.exists(frontend_path)}
