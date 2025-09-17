
# Restaurant Finder Coding Challenge

This project is a FastAPI-based service that takes a natural-language restaurant search query,
parses it into structured JSON using the Groq API, and prepares it for further search logic


## Requirements

* Python 3.9+
* Groq API Key (set in `.env`)
* Foursquare API Key (set in `.env`)

---

## Environment Variables

Create a `.env` file with the following:

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=your_groq_model_here
FOURSQUARE_API_KEY=your_fsq_key_here
ACCESS_CODE=your_access_code_here
```

---

## Installation & Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/carlrys/restaurant-finder.git
   cd restaurant-finder
   ```

2. Create a virtual environment & install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   uvicorn app:app --reload
   ```

---

## API Usage

### Endpoint: `/api/execute`

**Method:** `GET`

**Query Params:**

* `message`: Natural language input (e.g., `"Find me a cheap sushi restaurant in downtown Los Angeles that's open now and has at least a 4-star rating"`)
* `code`: Access code (from `.env`)

**Example Request:**

```bash
curl "http://127.0.0.1:8000/api/execute?message=Find%20me%20a%20cheap%20sushi%20restaurant%20in%20downtown%20Los%20Angeles%20that's%20open%20now%20and%20has%20at%20least%20a%204-star%20rating&code=pioneerdevai"
```


---

##  Docs to Read

* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [Uvicorn Docs](https://www.uvicorn.org/)
* [Groq API Reference](https://console.groq.com/docs)
* (Optional) [Foursquare Places API](https://location.foursquare.com/developer/reference/place-search)

---

## Limitations
* Since the use of Foursquare api service is free, some details may not be available
* Incorrect prompt may confuse LLM
* Regex might be unreliable

---

## Deployed Site/ URL to test
* https://restaurant-finder-challenge-carl.onrender.com/api/execute?message=Find%20me%20a%20cheap%20sushi%20restaurant%20in%20downtown%20Los%20Angeles%20that%27s%20open%20now%20and%20has%20at%20least%20a%204-star%20rating&code=pioneerdevai
