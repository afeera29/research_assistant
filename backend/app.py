from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
EXA_API_KEY = os.getenv("EXA_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Path to frontend build
frontend_build_dir = Path(__file__).parent.parent / "frontend" / "build"

# Serve static files
app.mount("/static", StaticFiles(directory=frontend_build_dir / "static"), name="static")

# API endpoint example
from exa_py import Exa
exa = Exa(EXA_API_KEY)

@app.get("/search")
async def search(query: str):
    response = exa.search(
        query,
        num_results=5,
        type='keyword'
    )
    results = []
    for result in response.results:
        results.append({
            "title": result.title,
            "author": getattr(result, "author", "N/A"),
            "date": getattr(result, "published_date", "N/A"),
            "url": result.url
        })
    return {"results": results}

# Serve React app
@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    index_file = frontend_build_dir / "index.html"
    return FileResponse(index_file)
