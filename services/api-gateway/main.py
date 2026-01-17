import requests
from fastapi import FastAPI, HTTPException

ORDER_URL="http://order-service:8000"
app=FastAPI(title="api-gateway")

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/checkout")
def checkout(item_id:str, quantity:int):
    try:
        r=requests.post(f"{ORDER_URL}/orders",
            params={"item_id":item_id,"quantity":quantity},timeout=3)
    except requests.exceptions.RequestException:
        raise HTTPException(503,"Order unreachable")
    if r.status_code!=200:
        raise HTTPException(r.status_code,r.text)
    return r.json()
