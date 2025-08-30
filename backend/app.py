from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
import requests
from exa_py import Exa
load_dotenv()

EXA_API_KEY = os.getenv("EXA_API_KEY")
exa = Exa(EXA_API_KEY) 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/build")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

@app.get("/")
def serve_react():
    return FileResponse(os.path.join(frontend_path, "index.html"))

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
