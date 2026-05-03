from fastapi import FastAPI, Body, Depends, HTTPException, Header
from genetic_algorithm import run_genetic_algorithm
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("WARNING: API_KEY environment variable not set")


@app.post("/recommend")
async def get_recommendations(payload: dict = Body(...), api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_profile = payload.get("user_profile")
    product_pool = payload.get("products")

    if product_pool is None:
        raise HTTPException(
            status_code=400, detail="Missing 'products' field in request body"
        )
    if user_profile is None:
        raise HTTPException(
            status_code=400, detail="Missing 'user_profile' field in request body"
        )

    best_suite = run_genetic_algorithm(product_pool, user_profile)
    return {"recommended_products": best_suite}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
