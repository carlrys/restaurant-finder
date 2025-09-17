import os
import httpx
from dotenv import load_dotenv

load_dotenv()

FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
FSQ_API_BASE = "https://places-api.foursquare.com"

async def fetch_restaurants(params: dict, limit: int=5):

    query = params.get("query")
    near = params.get("near")
    price = params.get("price")
    open_now = params.get("open_now")

    headers = {
        "Authorization": f"Bearer {FOURSQUARE_API_KEY}",
        "Accept": "application/json",
        "X-Places-Api-Version": "2025-06-17"
    }

    search_params = {
        "query": query,
        "near": near,
        "limit": limit
    }

    if price:
        search_params["price"] = price
    if open_now:
        search_params["open_now"] = open_now

    search_url = f"{FSQ_API_BASE}/places/search"

    results = []

    async with httpx.AsyncClient(headers=headers, timeout = 30.0) as client:
        response = await client.get(search_url,params=search_params)
        response.raise_for_status()
        data = response.json()

        for place in data.get("results", []):
            location = place.get("location", None)
            categories = place.get("categories", None)
            cuisine = ",".join(c.get("name") for c in categories) if categories else None

            results.append({
                "name": place.get("name", None),
                "address": ",".join(filter(None, [
                    location.get("address"),
                    location.get("locality"),
                    location.get("region"),
                    location.get("country")
                ])) or location.get("formatted_address"),
                "cuisine": cuisine,
                "rating": place.get("rating", None),
                "price": place.get("price", None),
                "hours": place.get("hours", None)
            })

    return results
