import os, random
from fastapi import FastAPI, HTTPException

FAIL_RATE=float(os.getenv("FAIL_RATE",0))
app=FastAPI(title="inventory-service")
STOCK={"item-1":10,"item-2":5}

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/ready")
def ready(): return {"ready":True}

@app.post("/reserve")
def reserve(item_id:str, quantity:int):
    if random.random()<FAIL_RATE:
        raise HTTPException(500,"DB timeout")
    if STOCK.get(item_id,0)<quantity:
        raise HTTPException(409,"Out of stock")
    STOCK[item_id]-=quantity
    return {"reserved":True}
