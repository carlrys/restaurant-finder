import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from services.llm_service import parse_message_to_json
from services.fsq_service import fetch_restaurants

load_dotenv()

ACCESS_CODE = os.getenv("ACCESS_CODE", "pioneerdevai")

app = FastAPI(title="Restaurant Finder")

@app.get("/api/execute")
async def execute(message: str = Query(...), code: str = Query(...)):
    if code != ACCESS_CODE:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        parsed = await parse_message_to_json(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM parsing failed: {e}")


    if not isinstance(parsed, dict) or parsed.get("action") != "restaurant_search":
        raise HTTPException(status_code=400, detail="LLM returned invalid action/structure")

    params = parsed.get("parameters", {})
    try:
        restaurants = await fetch_restaurants(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Foursquare error: {e}")

    return JSONResponse({"query": parsed, "restaurants": restaurants})
